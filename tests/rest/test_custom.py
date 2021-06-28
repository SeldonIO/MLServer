from mlserver.types import InferenceRequest


def test_custom_handler(rest_client, inference_request: InferenceRequest):
    response = rest_client.post("/my-custom-endpoint", json=[1, 2, 3, 4])

    assert response.status_code == 200
    assert response.json() == 10
