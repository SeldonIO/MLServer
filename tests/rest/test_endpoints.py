import pytest

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
    endpoint = f"v2/models/{sum_model_settings.name}"
    response = rest_client.get(endpoint)

    metadata = types.MetadataModelResponse.parse_obj(response.json())

    assert metadata.name == sum_model_settings.name
    assert metadata.platform == sum_model_settings.platform
    assert metadata.versions == sum_model_settings.versions
    assert metadata.inputs == sum_model_settings.inputs


@pytest.mark.parametrize(
    "model_name,model_version", [("sum-model", "v1.2.3"), ("sum-model", None)]
)
def test_infer(rest_client, inference_request, model_name, model_version):
    endpoint = f"/v2/models/{model_name}/infer"
    if model_version is not None:
        endpoint = f"/v2/models/{model_name}/versions/{model_version}/infer"
    response = rest_client.post(endpoint, json=inference_request.dict())

    assert response.status_code == 200

    prediction = types.InferenceResponse.parse_obj(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == [21]


def test_infer_error(rest_client, inference_request):
    endpoint = "/v2/models/my-model/versions/v0/infer"
    response = rest_client.post(endpoint, json=inference_request.dict())

    assert response.status_code == 400
    assert response.json()["error"] == "Model my-model with version v0 not found"


def test_model_repository_index(rest_client, repository_index_request):
    endpoint = "/v2/repository/index"
    response = rest_client.get(endpoint, json=repository_index_request.dict())

    assert response.status_code == 200

    models = response.json()
    assert len(models) == 1
