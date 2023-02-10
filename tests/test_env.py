import pytest
import sys
import os

from typing import List

from mlserver.env import Environment


async def test_from_tarball(env_tarball: str, tmp_path: str):
    env = await Environment.from_tarball(env_tarball, env_path=tmp_path)

    assert env.executable == os.path.join(tmp_path, "bin", "python")
    assert os.path.isfile(env.executable)


@pytest.mark.parametrize(
    "executable, expected",
    [
        ("/env/bin/python", "/env"),
        ("/env/bin/python3", "/env"),
        ("/envs/my-env/bin/python3", "/envs/my-env"),
    ],
)
def from_executable(executable: str, expected: str):
    env = Environment.from_executable(executable, (3, 8))
    assert env._env_path == expected
    assert env._version_info == (3, 8)


@pytest.mark.parametrize(
    "env, expected",
    [
        (
            Environment("/custom-environment/env", (3, 9)),
            [
                "/custom-environment/env/lib/python3.9.zip",
                "/custom-environment/env/lib/python3.9",
                "/custom-environment/env/lib/python3.9/lib-dynload",
                "/custom-environment/env/lib/python3.9/site-packages",
            ],
        ),
        (
            Environment("../", (3, 7)),
            [
                "../lib/python3.7.zip",
                "../lib/python3.7",
                "../lib/python3.7/lib-dynload",
                "../lib/python3.7/site-packages",
            ],
        ),
        (
            Environment("/", (3,)),
            [],
        ),
        (
            Environment("/", ()),
            [],
        ),
    ],
)
def test_get_sys_path(env: Environment, expected: List[str]):
    assert env.sys_path == expected


def test_get_bin_path():
    env = Environment("/env", (3, 9))
    assert env.bin_path == "/env/bin"


def test_activate_env():
    env = Environment("/envs/foo/my-custom-env", (3, 8))
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
