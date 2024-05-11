import asyncio
import aiohttp
import socket
import yaml

import os

from itertools import filterfalse

from asyncio import subprocess
from typing import List, Tuple

from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientOSError,
    ServerDisconnectedError,
)
from aiohttp_retry import RetryClient, ExponentialRetry

from mlserver.logging import logger
from mlserver.utils import generate_uuid
from mlserver.types import RepositoryIndexResponse, InferenceRequest, InferenceResponse


def get_available_ports(n: int = 1) -> List[int]:
    ports = set()

    while len(ports) < n:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()

        # The ports set will ensure there are no duplicates
        ports.add(port)

    return list(ports)


async def _run(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return_code = await process.wait()
    if return_code != 0:
        _, stderr = await process.communicate()
        logger.debug(f"Failed to run command '{cmd}'")
        logger.debug(stderr.decode("utf-8"))
        raise Exception(f"Command '{cmd}' failed with code '{return_code}'")


def _read_env(env_yml) -> dict:
    with open(env_yml, "r") as env_file:
        return yaml.safe_load(env_file.read())


def _write_env(env: dict, env_yml: str):
    with open(env_yml, "w") as env_file:
        env_file.write(yaml.dump(env))


def _is_python(dep: str) -> bool:
    return "python" in dep


def _inject_python_version(version: Tuple[int, int], env_yml: str) -> str:
    """
    To test the same environment.yml fixture we've got with different Python
    versions across environments, we inject dynamically the requested version.
    """
    env = _read_env(env_yml)
    major, minor = version
    without_python = list(filterfalse(_is_python, env["dependencies"]))
    with_env_python = [f"python == {major}.{minor}", *without_python]
    env["dependencies"] = with_env_python

    dst_folder = os.path.dirname(env_yml)
    new_env_yml = os.path.join(dst_folder, f"environment-py{major}{minor}.yml")
    _write_env(env, new_env_yml)
    return new_env_yml


async def _pack(version: Tuple[int, int], env_yml: str, tarball_path: str):
    uuid = generate_uuid()
    fixed_env_yml = _inject_python_version(version, env_yml)
    env_name = f"mlserver-{uuid}"
    try:
        await _run(f"conda env create -n {env_name} -f {fixed_env_yml}")
        # NOTE: We exclude Python's symlink into 3.1 for >=3.10
        # See https://github.com/conda/conda-pack/issues/244#issuecomment-1361094094
        await _run(
            "conda-pack"
            " --ignore-missing-files "
            " --exclude lib/python3.1"
            f" -n {env_name}"
            f" -o {tarball_path}"
        )
    finally:
        await _run(f"conda env remove -n {env_name}")


def _get_tarball_name(version: Tuple[int, int]) -> str:
    major, minor = version
    return f"environment-py{major}{minor}.tar.gz"


class RESTClient:
    def __init__(self, http_server: str):
        self._session = aiohttp.ClientSession(raise_for_status=True)
        self._http_server = http_server

    async def close(self):
        await self._session.close()

    async def _retry_get(self, endpoint: str):
        retry_options = ExponentialRetry(
            attempts=10,
            start_timeout=0.5,
            statuses=[400],
            exceptions={
                ClientConnectorError,
                ClientOSError,
                ServerDisconnectedError,
                ConnectionRefusedError,
            },
        )
        retry_client = RetryClient(raise_for_status=True, retry_options=retry_options)

        async with retry_client:
            await retry_client.get(endpoint)

    async def wait_until_ready(self) -> None:
        endpoint = f"http://{self._http_server}/v2/health/ready"
        await self._retry_get(endpoint)

    async def wait_until_model_ready(self, model_name: str) -> None:
        endpoint = f"http://{self._http_server}/v2/models/{model_name}/ready"
        await self._retry_get(endpoint)

    async def wait_until_live(self) -> None:
        endpoint = f"http://{self._http_server}/v2/health/live"
        await self._retry_get(endpoint)

    async def ready(self) -> bool:
        endpoint = f"http://{self._http_server}/v2/health/ready"
        res = await self._session.get(endpoint)
        return res.status == 200

    async def live(self) -> bool:
        endpoint = f"http://{self._http_server}/v2/health/live"
        res = await self._session.get(endpoint)
        return res.status == 200

    async def list_models(self) -> RepositoryIndexResponse:
        endpoint = f"http://{self._http_server}/v2/repository/index"
        response = await self._session.post(endpoint, json={"ready": True})

        raw_payload = await response.text()
        return RepositoryIndexResponse.parse_raw(raw_payload)

    async def infer(
        self, model_name: str, inference_request: InferenceRequest
    ) -> InferenceResponse:
        endpoint = f"http://{self._http_server}/v2/models/{model_name}/infer"
        response = await self._session.post(
            endpoint, json=inference_request.model_dump()
        )

        raw_payload = await response.text()
        return InferenceResponse.parse_raw(raw_payload)
