"""
Utilities to work with custom environments.
"""
import os

from typing import List

from .logging import logger


def get_sys_path(executable: str, version_info: tuple) -> List[str]:
    """
    Returns list of PYTHONPATH (i.e. `sys.path`) to add to the environment for
    a given Python binary.
    This ensures that custom environments get loaded correctly.
    """
    if len(version_info) < 2:
        logger.warning(
            "Invalid version info. Expected, at least, two dimensions "
            f"(i.e. (major, minor, ...)) but got {version_info}"
        )
        return []

    env_path = os.path.dirname(os.path.dirname(executable))
    major = version_info[0]
    minor = version_info[1]
    lib_path = os.path.join(env_path, "lib", f"python{major}.{minor}")

    return [
        f"{lib_path}.zip",
        lib_path,
        os.path.join(lib_path, "lib-dynload"),
        os.path.join(lib_path, "site-packages"),
    ]


def get_bin_path(executable: str) -> str:
    """
    Returns `./bin` path from custom environment (to be added to PATH env var).
    This ensures that CLI binaries (e.g. Conda-installed Java) are available in
    custom environments.
    """
    return os.path.dirname(executable)
