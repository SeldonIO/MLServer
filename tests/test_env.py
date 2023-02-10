import pytest
import sys
import os
import shutil

from typing import List

from mlserver.env import Environment


async def test_from_tarball(env_tarball: str, tmp_path: str):
    env = await Environment.from_tarball(env_tarball, env_path=tmp_path)

    executable = os.path.join(tmp_path, "bin", "python")
    assert os.path.isfile(executable)
    assert os.path.isdir(env.lib_path)


def test_sys_path(env: Environment):
    expected = [
        #  f"{env._env_path}/lib/python3.9.zip",
        #  f"{env._env_path}/lib/python3.9",
        #  f"{env._env_path}/lib/python3.9/lib-dynload",
        f"{env._env_path}/lib/python3.9/site-packages",
    ]
    assert env.sys_path == expected


def test_sys_path_empty(env: Environment):
    # Force lib_path to be empty
    env.__dict__["lib_path"] = ""
    expected = []
    assert env.sys_path == expected


@pytest.mark.parametrize(
    "folder_name",
    ["python3.9", "python37", "python3.11", ""],
)
def test_lib_path(env: Environment, folder_name: str):
    default_lib_path = env.lib_path
    assert default_lib_path == f"{env._env_path}/lib/python3.9"

    if folder_name:
        base_path = os.path.dirname(default_lib_path)
        expected_path = os.path.join(base_path, folder_name)
        os.rename(default_lib_path, expected_path)
    else:
        shutil.rmtree(default_lib_path)
        expected_path = ""

    # Force to look again for lib_path
    del env.__dict__["lib_path"]
    assert env.lib_path == expected_path


def test_bin_path(env: Environment):
    assert env.bin_path == f"{env._env_path}/bin"


def test_activate_env(env: Environment):
    assert env._env_path not in ",".join(sys.path)
    assert env._env_path not in os.environ["PATH"]

    with env:
        sys_path = env.sys_path
        assert sys_path

        for i, p in enumerate(sys_path):
            assert sys.path[i] == p

        bin_paths = os.environ["PATH"].split(os.pathsep)
        assert bin_paths[0] == env.bin_path

    assert env._env_path not in ",".join(sys.path)
    assert env._env_path not in os.environ["PATH"]
