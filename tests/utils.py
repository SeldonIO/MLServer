import aiohttp
import socket

from aiohttp.client_exceptions import ClientOSError, ServerDisconnectedError
from aiohttp_retry import RetryClient, ExponentialRetry

from mlserver.types import RepositoryIndexResponse, InferenceRequest, InferenceResponse


def get_available_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class RESTClient:
    def __init__(self, http_server: str):
        self._session = aiohttp.ClientSession(raise_for_status=True)
        self._http_server = http_server

    async def close(self):
        await self._session.close()

    async def wait_until_ready(self) -> None:
        endpoint = f"http://{self._http_server}/v2/health/ready"
        retry_options = ExponentialRetry(
            attempts=10,
            start_timeout=0.5,
            exceptions={ClientOSError, ServerDisconnectedError},
        )
        retry_client = RetryClient(raise_for_status=True, retry_options=retry_options)

        async with retry_client:
            await retry_client.get(endpoint, raise_for_status=True)

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
