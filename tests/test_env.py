import pytest

from typing import List

from mlserver.env import get_sys_path, get_bin_path


@pytest.mark.parametrize(
    "executable, version_info, expected",
    [
        (
            "/custom-environment/env/bin/python",
            (3, 9),
            [
                "/custom-environment/env/lib/python3.9.zip",
                "/custom-environment/env/lib/python3.9",
                "/custom-environment/env/lib/python3.9/lib-dynload",
                "/custom-environment/env/lib/python3.9/site-packages",
            ],
        ),
        (
            "../bin/python",
            (3, 7),
            [
                "../lib/python3.7.zip",
                "../lib/python3.7",
                "../lib/python3.7/lib-dynload",
                "../lib/python3.7/site-packages",
            ],
        ),
        (
            "/bin/python",
            (3,),
            [],
        ),
        (
            "/bin/python",
            (),
            [],
        ),
    ],
)
def test_get_sys_path(executable: str, version_info: tuple, expected: List[str]):
    sys_path = get_sys_path(executable, version_info)
    assert sys_path == expected


def test_get_bin_path():
    executable = "/env/bin/python"
    path = get_bin_path(executable)
    assert path == "/env/bin"
