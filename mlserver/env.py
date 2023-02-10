import asyncio
import os
import sys
import tarfile
import glob

from typing import Optional, List, Tuple
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

    def __init__(self, env_path: str) -> "Environment":
        self._env_path = env_path

    @classmethod
    async def from_tarball(cls, tarball_path: str, env_path: str) -> "Environment":
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _extract_env, tarball_path, env_path)

        return cls(env_path)

    @cached_property
    def sys_path(self) -> List[str]:
        if not self.lib_path:
            return []

        # NOTE: We will only expose the modules within `site-packages`.
        # This modules are those installed by the user, and don't include
        # Python system libraries.
        # That way, we will keep using the Python version and modules from the
        # main MLServer process.
        # In the future, we may want to allow for a "global" custom env that
        # also changes Python's system libraries - however, at the moment that
        # breaks the dispatcher <-> worker pipeline.
        return [
            #  f"{self.lib_path}.zip",
            #  self.lib_path,
            #  os.path.join(self.lib_path, "lib-dynload"),
            os.path.join(self.lib_path, "site-packages"),
        ]

    @cached_property
    def bin_path(self) -> str:
        return os.path.join(self._env_path, "bin")

    @cached_property
    def lib_path(self) -> str:
        pattern = os.path.join(self._env_path, "lib", "python*")
        matches = glob.glob(pattern)

        for match in matches:
            if os.path.isdir(match):
                return match

        return ""

    def __enter__(self):
        self._prev_sys_path = sys.path
        self._prev_bin_path = os.environ["PATH"]

        sys.path = [*self.sys_path, *self._prev_sys_path]
        os.environ["PATH"] = os.pathsep.join([self.bin_path, self._prev_bin_path])

        return self

    def __exit__(self, *exc_details) -> None:
        sys.path = self._prev_sys_path
        os.environ["PATH"] = self._prev_bin_path
