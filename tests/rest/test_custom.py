from mlserver.types import InferenceRequest
import gzip
import json


async def test_custom_handler(
    rest_client,
):
    response = await rest_client.post("/my-custom-endpoint", json=[1, 2, 3, 4])

    assert response.status_code == 200
    assert response.json() == 10


async def test_custom_handler_gzip(rest_client, inference_request: InferenceRequest):
    response = await rest_client.post(
        "/my-custom-endpoint",
        content=gzip.compress(json.dumps([1, 2, 3, 4]).encode("utf-8")),
        headers={"Content-Encoding": "gzip"},
    )

    assert response.status_code == 200
    assert response.json() == 10


async def test_gzip_compression(
    rest_client,
    inference_request,
    sum_model_settings,
):
    endpoint = "/custom-endpoint-with-long-response"
    response = await rest_client.post(
        endpoint, json=1000, headers={"accept-encoding": "gzip"}
    )

    assert response.status_code == 200
    assert "content-encoding" in response.headers
    assert response.headers["content-encoding"] == "gzip"
    assert "foo" in response.json()
