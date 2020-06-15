from mlserver import types


def test_live(rest_client):
    endpoint = "/v2/health/live"
    response = rest_client.get(endpoint)

    assert response.status_code == 200


def test_ready(rest_client):
    endpoint = "/v2/health/ready"
    response = rest_client.get(endpoint)

    assert response.status_code == 200


def test_model_ready(rest_client, sum_model):
    version = "1.2.3"
    endpoint = f"/v2/models/{sum_model.name}/versions/{version}/ready"
    response = rest_client.get(endpoint)

    assert response.status_code == 200


def test_infer(rest_client, sum_model, inference_request):
    version = "1.2.3"
    endpoint = f"/v2/models/{sum_model.name}/versions/{version}/infer"
    response = rest_client.post(endpoint, json=inference_request.dict())

    expected = types.TensorData.parse_obj([21.0])

    assert response.status_code == 200

    prediction = types.InferenceResponse.parse_obj(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == expected
