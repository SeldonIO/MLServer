import asyncio
import os
import sys
import tarfile
import glob

from typing import List
from functools import cached_property

from .logging import logger


def _extract_env(tarball_path: str, env_path: str) -> None:
    logger.info(f"Extracting environment tarball from {tarball_path}...")
    with tarfile.open(tarball_path, "r") as tarball:
        tarball.extractall(path=env_path)


class Environment:
    """
    Custom Python environment.
    The class can be used as a context manager to enable / disable the custom
    environment.
    """

    def __init__(self, env_path: str):
        self._env_path = env_path

    @classmethod
    async def from_tarball(cls, tarball_path: str, env_path: str) -> "Environment":
        """
        Instantiate an Environment object from an environment tarball.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _extract_env, tarball_path, env_path)

        return cls(env_path)

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
