from mlserver import types, __version__


def test_live(rest_client):
    endpoint = "/v2/health/live"
    response = rest_client.get(endpoint)

    assert response.status_code == 200


def test_ready(rest_client):
    endpoint = "/v2/health/ready"
    response = rest_client.get(endpoint)

    assert response.status_code == 200


def test_model_ready(rest_client, sum_model):
    endpoint = f"/v2/models/{sum_model.name}/versions/{sum_model.version}/ready"
    response = rest_client.get(endpoint)

    assert response.status_code == 200


def test_metadata(rest_client):
    endpoint = "/v2"
    response = rest_client.get(endpoint)

    metadata = types.MetadataServerResponse.parse_obj(response.json())

    assert metadata.name == "mlserver"
    assert metadata.version == __version__
    assert metadata.extensions == []


def test_model_metadata(rest_client, sum_model_settings):
    endpoint = (
        f"v2/models/{sum_model_settings.name}/versions/{sum_model_settings.version}"
    )
    response = rest_client.get(endpoint)

    metadata = types.MetadataModelResponse.parse_obj(response.json())

    assert metadata.name == sum_model_settings.name
    assert metadata.platform == sum_model_settings.platform
    assert metadata.versions == sum_model_settings.versions
    assert metadata.inputs == sum_model_settings.inputs


def test_infer(rest_client, sum_model, inference_request):
    endpoint = f"/v2/models/{sum_model.name}/versions/{sum_model.version}/infer"
    response = rest_client.post(endpoint, json=inference_request.dict())

    assert response.status_code == 200

    prediction = types.InferenceResponse.parse_obj(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == [21]
