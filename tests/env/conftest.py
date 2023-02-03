import asyncio
import pytest
import shutil
import os

from asyncio import subprocess
from mlserver.utils import generate_uuid
from mlserver.logging import logger

from ..conftest import TESTDATA_PATH

TESTDATA_CACHE_PATH = os.path.join(TESTDATA_PATH, ".cache")


async def _run(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return_code = await process.wait()
    if return_code != 0:
        raise Exception(f"Command '{cmd}' failed with code '{return_code}'")


async def _pack(env_yml: str, tarball_path: str):
    uuid = generate_uuid()
    env_name = f"mlserver-{uuid}"
    try:
        await _run(f"conda env create -n {env_name} -f {env_yml}")
        await _run(f"conda-pack --ignore-missing-files -n {env_name} -o {tarball_path}")
    finally:
        await _run(f"conda env remove -n {env_name}")


@pytest.fixture
async def env_tarball(tmp_path: str) -> str:
    tarball_path = os.path.join(TESTDATA_CACHE_PATH, "environment.tar.gz")
    if os.path.isfile(tarball_path):
        return tarball_path

    os.makedirs(TESTDATA_CACHE_PATH, exist_ok=True)
    env_yml = os.path.join(TESTDATA_PATH, "environment.yml")
    await _pack(env_yml, tarball_path)
    return tarball_path
