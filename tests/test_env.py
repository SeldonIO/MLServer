import pytest
import sys
import os
import shutil

from typing import Tuple

from mlserver.env import Environment, compute_hash_of_file


@pytest.fixture
def expected_python_folder(env_python_version: Tuple[int, int]) -> str:
    major, minor = env_python_version
    return f"python{major}.{minor}"


async def test_compute_hash(env_tarball: str):
    env_hash = await compute_hash_of_file(env_tarball)
    assert len(env_hash) == 64


async def test_from_tarball(env_tarball: str, tmp_path: str):
    env = await Environment.from_tarball(env_tarball, env_path=tmp_path)

    executable = os.path.join(tmp_path, "bin", "python")
    assert os.path.isfile(executable)
    assert os.path.isdir(env._lib_path)
    assert len(env.env_hash) == 64


def test_sys_path(env: Environment, expected_python_folder: str):
    expected = [
        f"{env._env_path}/lib/{expected_python_folder}.zip",
        f"{env._env_path}/lib/{expected_python_folder}",
        f"{env._env_path}/lib/{expected_python_folder}/lib-dynload",
        f"{env._env_path}/lib/{expected_python_folder}/site-packages",
    ]
    assert env._sys_path == expected


def test_sys_path_empty(env: Environment):
    # Force lib_path to be empty
    env.__dict__["_lib_path"] = ""
    expected = []
    assert env._sys_path == expected


@pytest.mark.parametrize(
    "folder_name",
    ["python3.9", "python3.11", "python3.12"],
)
def test_lib_path(env: Environment, folder_name: str, expected_python_folder: str):
    default_lib_path = env._lib_path
    assert default_lib_path == f"{env._env_path}/lib/{expected_python_folder}"

    if folder_name:
        base_path = os.path.dirname(default_lib_path)
        expected_path = os.path.join(base_path, folder_name)
        os.rename(default_lib_path, expected_path)
    else:
        shutil.rmtree(env._lib_path)
        expected_path = ""

    # Force to look again for lib_path
    del env.__dict__["_lib_path"]
    assert env._lib_path == expected_path


def test_bin_path(env: Environment):
    assert env._bin_path == f"{env._env_path}/bin"


def test_exec_path(env: Environment):
    assert env._exec_path == f"{env._env_path}/bin/python"


def test_activate_env(env: Environment):
    assert env._env_path not in ",".join(sys.path)
    assert env._env_path not in os.environ["PATH"]

    with env:
        sys_path = env._sys_path
        assert sys_path

        for i, p in enumerate(sys_path):
            assert sys.path[i] == p

        bin_paths = os.environ["PATH"].split(os.pathsep)
        assert bin_paths[0] == env._bin_path

        exec_path = os.path.join(bin_paths[0], "python")
        assert exec_path == env._exec_path

    assert env._env_path not in ",".join(sys.path)
    assert env._env_path not in os.environ["PATH"]
