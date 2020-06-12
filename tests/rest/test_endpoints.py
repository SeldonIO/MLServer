from mlserver import types


def test_infer(rest_client, sum_model, inference_request):
    version = "1.2.3"
    endpoint = f"/v2/models/{sum_model.name}/versions/{version}/infer"
    response = rest_client.post(endpoint, json=inference_request.dict())

    expected = types.TensorData.parse_obj([21.0])

    assert response.status_code == 200

    prediction = types.InferenceResponse.parse_obj(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == expected
