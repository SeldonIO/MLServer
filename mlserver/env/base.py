import asyncio
import os
import sys
import tarfile

from typing import Optional, List, Tuple

from ..logging import logger


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

    def __init__(self, env_path: str, version_info: Tuple[str] = None) -> "Environment":
        self._env_path = env_path
        self.version_info = version_info

    @classmethod
    def from_executable(cls, executable: str, version_info: tuple) -> "Environment":
        """
        Alternative constructor to instantiate an environment from the Python
        bin executable (rather than the env path).
        """
        env_path = os.path.dirname(os.path.dirname(executable))
        return cls(env_path, version_info)

    @classmethod
    async def from_tarball(cls, tarball_path: str, env_path: str) -> "Environment":
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _extract_env, tarball_path, env_path)

        return cls(env_path)

    @property
    def executable(self) -> str:
        return os.path.join(self._env_path, "bin", "python")

    @property
    def sys_path(self) -> List[str]:
        if len(self.version_info) < 2:
            return []

        major = self.version_info[0]
        minor = self.version_info[1]
        lib_path = os.path.join(self._env_path, "lib", f"python{major}.{minor}")

        return [
            f"{lib_path}.zip",
            lib_path,
            os.path.join(lib_path, "lib-dynload"),
            os.path.join(lib_path, "site-packages"),
        ]

    @property
    def bin_path(self) -> str:
        return os.path.join(self._env_path, "bin")

    @property
    def version_info(self) -> Tuple[str]:
        if self._version_info is None:
            return ()

        return self._version_info

    @version_info.setter
    def version_info(self, v: Optional[Tuple[str]]):
        if v is not None and len(v) < 2:
            logger.warning(
                "Invalid version info. Expected, at least, two dimensions "
                f"(i.e. (major, minor, ...)) but got {v}"
            )

        self._version_info = v

    def __enter__(self):
        self._prev_sys_path = sys.path
        self._prev_bin_path = os.environ["PATH"]

        sys.path = [*self.sys_path, *self._prev_sys_path]
        os.environ["PATH"] = os.pathsep.join([self.bin_path, self._prev_bin_path])

        return self

    def __exit__(self, *exc_details) -> None:
        sys.path = self._prev_sys_path
        os.environ["PATH"] = self._prev_bin_path
