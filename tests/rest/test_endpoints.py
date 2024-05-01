import pytest

from typing import Optional

from mlserver import __version__
from mlserver.types import (
    InferenceResponse,
    MetadataServerResponse,
    MetadataModelResponse,
    TensorData,
)
from mlserver.cloudevents import (
    CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT,
    CLOUDEVENTS_HEADER_SPECVERSION,
)


async def test_live(rest_client):
    endpoint = "/v2/health/live"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200


async def test_ready(rest_client):
    endpoint = "/v2/health/ready"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200


async def test_model_ready(rest_client, sum_model):
    endpoint = f"/v2/models/{sum_model.name}/versions/{sum_model.version}/ready"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200


async def test_metadata(rest_client):
    endpoint = "/v2"
    response = await rest_client.get(endpoint)

    metadata = MetadataServerResponse.model_validate(response.json())

    assert metadata.name == "mlserver"
    assert metadata.version == __version__
    assert metadata.extensions == []


async def test_openapi(rest_client):
    endpoint = "/v2/docs"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert "html" in response.headers["content-type"]


async def test_docs(rest_client):
    endpoint = "/v2/docs/dataplane.json"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert "openapi" in response.json()


async def test_model_metadata(rest_client, sum_model_settings):
    endpoint = f"v2/models/{sum_model_settings.name}"
    response = await rest_client.get(endpoint)

    metadata = MetadataModelResponse.model_validate(response.json())

    assert metadata.name == sum_model_settings.name
    assert metadata.platform == sum_model_settings.platform
    assert metadata.versions == sum_model_settings.versions
    assert metadata.inputs == sum_model_settings.inputs


@pytest.mark.parametrize(
    "model_name,model_version", [("sum-model", "v1.2.3"), ("sum-model", None)]
)
async def test_model_openapi(
    rest_client, model_name: str, model_version: Optional[str]
):
    endpoint = f"/v2/models/{model_name}/docs/dataplane.json"
    if model_version is not None:
        endpoint = (
            f"/v2/models/{model_name}/versions/{model_version}/docs/dataplane.json"
        )
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert "openapi" in response.json()


@pytest.mark.parametrize(
    "model_name,model_version", [("sum-model", "v1.2.3"), ("sum-model", None)]
)
async def test_model_docs(rest_client, model_name: str, model_version: Optional[str]):
    endpoint = f"/v2/models/{model_name}/docs"
    if model_version is not None:
        endpoint = f"/v2/models/{model_name}/versions/{model_version}/docs"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert "html" in response.headers["content-type"]


@pytest.mark.parametrize(
    "model_name,model_version", [("sum-model", "v1.2.3"), ("sum-model", None)]
)
async def test_infer(
    rest_client,
    inference_request,
    model_name,
    model_version,
):
    endpoint = f"/v2/models/{model_name}/infer"
    if model_version is not None:
        endpoint = f"/v2/models/{model_name}/versions/{model_version}/infer"
    response = await rest_client.post(endpoint, json=inference_request.dict())

    assert response.status_code == 200

    prediction = InferenceResponse.model_validate(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == TensorData(root=[6])


async def test_infer_headers(
    rest_client,
    inference_request,
    sum_model_settings,
):
    endpoint = f"/v2/models/{sum_model_settings.name}/infer"
    response = await rest_client.post(
        endpoint, json=inference_request.dict(), headers={"x-foo": "bar"}
    )

    assert response.status_code == 200
    assert "x-foo" in response.headers
    assert response.headers["x-foo"] == "bar"

    assert CLOUDEVENTS_HEADER_SPECVERSION in response.headers
    assert (
        response.headers[CLOUDEVENTS_HEADER_SPECVERSION]
        == CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT
    )


async def test_infer_error(rest_client, inference_request):
    endpoint = "/v2/models/my-model/versions/v0/infer"
    response = await rest_client.post(endpoint, json=inference_request.dict())

    assert response.status_code == 404
    assert response.json()["error"] == "Model my-model with version v0 not found"


async def test_model_repository_index(rest_client, repository_index_request):
    endpoint = "/v2/repository/index"
    response = await rest_client.post(endpoint, json=repository_index_request.dict())

    assert response.status_code == 200

    models = response.json()
    assert len(models) == 1


async def test_model_repository_unload(rest_client, sum_model_settings):
    endpoint = f"/v2/repository/models/{sum_model_settings.name}/unload"
    response = await rest_client.post(endpoint)

    assert response.status_code == 200

    model_metadata = await rest_client.get(f"/v2/models/{sum_model_settings.name}")
    assert model_metadata.status_code == 404


async def test_model_repository_load(
    rest_client,
    sum_model_settings,
):
    await rest_client.post(f"/v2/repository/models/{sum_model_settings.name}/unload")

    endpoint = f"/v2/repository/models/{sum_model_settings.name}/load"
    response = await rest_client.post(endpoint)

    assert response.status_code == 200

    model_metadata = await rest_client.get(f"/v2/models/{sum_model_settings.name}")
    assert model_metadata.status_code == 200


async def test_model_repository_load_error(rest_client, sum_model_settings):
    endpoint = "/v2/repository/models/my-model/load"
    response = await rest_client.post(endpoint)

    assert response.status_code == 404
    assert response.json()["error"] == "Model my-model not found"


async def test_infer_invalid_datatype_error(
    rest_client, inference_request_invalid_datatype, datatype_error_message
):
    endpoint = "/v2/models/sum-model/infer"
    response = await rest_client.post(endpoint, json=inference_request_invalid_datatype)

    assert response.status_code == 422

    assert response.json()["detail"][0]["msg"] == datatype_error_message
