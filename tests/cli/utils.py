import aiohttp

from aiohttp_retry import RetryClient, ExponentialRetry

from mlserver.types import RepositoryIndexResponse, InferenceRequest, InferenceResponse


class APIClient:
    def __init__(self, http_server: str):
        self._session = aiohttp.ClientSession(raise_for_status=True)
        self._http_server = http_server

    async def wait_until_ready(self) -> None:
        endpoint = f"http://{self._http_server}/v2/health/ready"
        retry_options = ExponentialRetry(attempts=3)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options)

        with retry_client:
            await retry_client.get(endpoint, raise_for_status=True)

    async def list_models(self) -> RepositoryIndexResponse:
        endpoint = f"http://{self._http_server}/v2/repository/index"
        response = await self._session.post(endpoint, json={"ready": True})

        return RepositoryIndexResponse.from_raw(response.text)

    async def infer(
        self, model_name: str, inference_request: InferenceRequest
    ) -> InferenceResponse:
        endpoint = f"http://{self._http_server}/v2/models/{model_name}/infer"
        response = await self._session.post(endpoint, json=inference_request.dict())
        return InferenceResponse.parse_raw(response.text)
