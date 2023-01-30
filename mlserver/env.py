"""
Utilities to work with custom environments.
"""
import os
import sys

from typing import List

from .logging import logger


class Environment:
    def __init__(self, env_path: str, version_info: tuple):
        if len(version_info) < 2:
            logger.warning(
                "Invalid version info. Expected, at least, two dimensions "
                f"(i.e. (major, minor, ...)) but got {version_info}"
            )

        self._env_path = env_path
        self._version_info = version_info

    @classmethod
    def from_executable(cls, executable: str, version_info: tuple) -> "Environment":
        env_path = os.path.dirname(os.path.dirname(executable))
        return cls(env_path, version_info)

    @property
    def sys_path(self) -> List[str]:
        if len(self._version_info) < 2:
            return []

        major = self._version_info[0]
        minor = self._version_info[1]
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


def activate_env(env_path: str):
    sys_path = _get_sys_path(env_path)
    sys.path = [*sys_path, sys.path]

    bin_path = _get_bin_path(env_path)
    prev_path = os.environ["PATH"]
    os.environ["PATH"] = os.pathsep.join(bin_path, prev_path)
