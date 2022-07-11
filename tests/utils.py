import aiohttp
import socket

from typing import List

from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientOSError,
    ServerDisconnectedError,
)
from aiohttp_retry import RetryClient, ExponentialRetry

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
            exceptions={ClientConnectorError, ClientOSError, ServerDisconnectedError},
        )
        retry_client = RetryClient(raise_for_status=True, retry_options=retry_options)

        async with retry_client:
            await retry_client.get(endpoint, raise_for_status=True)

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
        response = await self._session.post(endpoint, json=inference_request.dict())

        raw_payload = await response.text()
        return InferenceResponse.parse_raw(raw_payload)
