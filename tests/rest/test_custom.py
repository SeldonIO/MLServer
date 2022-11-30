from mlserver.types import InferenceRequest
from ..metrics.conftest import prometheus_registry
from prometheus_client.registry import CollectorRegistry


async def test_custom_handler(
    prometheus_registry: CollectorRegistry,
    rest_client,
    inference_request: InferenceRequest,
):
    response = await rest_client.post("/my-custom-endpoint", json=[1, 2, 3, 4])

    assert response.status_code == 200
    assert response.json() == 10


async def test_gzip_compression(
    prometheus_registry: CollectorRegistry,
    rest_client,
    inference_request,
    sum_model_settings,
):
    endpoint = "/custom-endpoint-with-long-response"
    response = await rest_client.post(
        endpoint, params={"length": 1000}, headers={"accept-encoding": "gzip"}
    )

    assert response.status_code == 200
    assert "content-encoding" in response.headers
    assert response.headers["content-encoding"] == "gzip"
    assert "foo" in response.json()
