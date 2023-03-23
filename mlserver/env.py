import asyncio
import os
import sys
import tarfile
import glob
import hashlib

from typing import List, Optional
from functools import cached_property

from .logging import logger


def _extract_env(tarball_path: str, env_path: str) -> None:
    logger.info(f"Extracting environment tarball from {tarball_path}...")
    with tarfile.open(tarball_path, "r") as tarball:
        tarball.extractall(path=env_path)


def _compute_hash(tarball_path: str) -> str:
    """
    From Python 3.11's implementation of `hashlib.file_digest()`:
    https://github.com/python/cpython/blob/3.11/Lib/hashlib.py#L257
    """
    h = hashlib.sha256()
    buffer_size = 2**18

    # Disable IO buffering since it's handled explicitly below
    with open(tarball_path, "rb", buffering=0) as env_file:
        buffer = bytearray(buffer_size)
        view = memoryview(buffer)
        while True:
            size = env_file.readinto(buffer)
            if size == 0:
                break
            h.update(view[:size])

    return h.hexdigest()


async def compute_hash(tarball_path: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _compute_hash, tarball_path)


class Environment:
    """
    Custom Python environment.
    The class can be used as a context manager to enable / disable the custom
    environment.
    """

    def __init__(self, env_path: str, env_hash: str):
        self._env_path = env_path
        self.env_hash = env_hash

    @classmethod
    async def from_tarball(
        cls, tarball_path: str, env_path: str, env_hash: Optional[str] = None
    ) -> "Environment":
        """
        Instantiate an Environment object from an environment tarball.
        If the env hash is not provided, it will be computed on-the-fly.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _extract_env, tarball_path, env_path)

        if not env_hash:
            env_hash = await compute_hash(tarball_path)

        return cls(env_path, env_hash)

    @cached_property
    def _sys_path(self) -> List[str]:
        """
        Extra paths that will be added to `sys.path` (i.e. `PYTHONPATH`) to
        expose the custom environment.
        These paths are mainly used on the `__enter__` method of the context
        manager below.
        """
        if not self._lib_path:
            return []

        # This list of paths is mainly built from PEP370 (and also from how
        # PYTHONPATH is defined by default).
        # The main route is probably just `.../site-packages`, but we add the
        # rest to be safe.
        return [
            f"{self._lib_path}.zip",
            self._lib_path,
            os.path.join(self._lib_path, "lib-dynload"),
            os.path.join(self._lib_path, "site-packages"),
        ]

    @cached_property
    def _bin_path(self) -> str:
        """
        Path to the `../bin/` folder in our custom environment.
        """
        return os.path.join(self._env_path, "bin")

    @cached_property
    def _lib_path(self) -> str:
        """
        Base environment path (i.e. user data directory - as defined by
        PEP370).
        """
        pattern = os.path.join(self._env_path, "lib", "python*")
        matches = glob.glob(pattern)

        for match in matches:
            if os.path.isdir(match):
                return match

        return ""

    def __enter__(self):
        self._prev_sys_path = sys.path
        self._prev_bin_path = os.environ["PATH"]

        sys.path = [*self._sys_path, *self._prev_sys_path]
        os.environ["PATH"] = os.pathsep.join([self._bin_path, self._prev_bin_path])

        return self

    def __exit__(self, *exc_details) -> None:
        sys.path = self._prev_sys_path
        os.environ["PATH"] = self._prev_bin_path
