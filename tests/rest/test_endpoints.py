import pytest
from pytest_lazyfixture import lazy_fixture

from typing import Optional
from httpx import AsyncClient
from httpx_sse import aconnect_sse

from mlserver import __version__
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    MetadataServerResponse,
    MetadataModelResponse,
<<<<<<< HEAD
    TensorData,
=======
    RepositoryIndexRequest,
>>>>>>> Add tests for infer-stream endpoint
)
from mlserver.cloudevents import (
    CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT,
    CLOUDEVENTS_HEADER_SPECVERSION,
)


async def test_live(rest_client: AsyncClient):
    endpoint = "/v2/health/live"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200


async def test_ready(rest_client: AsyncClient):
    endpoint = "/v2/health/ready"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200


async def test_model_ready(rest_client: AsyncClient, sum_model: MLModel):
    endpoint = f"/v2/models/{sum_model.name}/versions/{sum_model.version}/ready"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200


async def test_metadata(rest_client: AsyncClient):
    endpoint = "/v2"
    response = await rest_client.get(endpoint)

    metadata = MetadataServerResponse.model_validate(response.json())

    assert metadata.name == "mlserver"
    assert metadata.version == __version__
    assert metadata.extensions == []


async def test_openapi(rest_client: AsyncClient):
    endpoint = "/v2/docs"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert "html" in response.headers["content-type"]


async def test_docs(rest_client: AsyncClient):
    endpoint = "/v2/docs/dataplane.json"
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert "openapi" in response.json()


async def test_model_metadata(
    rest_client: AsyncClient, sum_model_settings: ModelSettings
):
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
    rest_client: AsyncClient, model_name: str, model_version: Optional[str]
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
async def test_model_docs(
    rest_client: AsyncClient, model_name: str, model_version: Optional[str]
):
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
    rest_client: AsyncClient,
    inference_request: InferenceRequest,
    model_name: str,
    model_version: Optional[str],
):
    endpoint = f"/v2/models/{model_name}/infer"
    if model_version is not None:
        endpoint = f"/v2/models/{model_name}/versions/{model_version}/infer"
<<<<<<< HEAD
    response = await rest_client.post(endpoint, json=inference_request.model_dump())
=======
>>>>>>> Included endpoint tests for generate and generate_stream.

    response = await rest_client.post(endpoint, json=inference_request.dict())
    assert response.status_code == 200

    prediction = InferenceResponse.model_validate(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == TensorData(root=[6])


@pytest.mark.parametrize("sum_model", [lazy_fixture("text_model")])
@pytest.mark.parametrize(
    "model_name,model_version", [("text-model", "v1.2.3"), ("text-model", None)]
)
async def test_generate(
    rest_client: AsyncClient,
    generate_request: InferenceRequest,
    model_name: str,
    model_version: Optional[str],
):
    endpoint = f"/v2/models/{model_name}/generate"
    if model_version is not None:
        endpoint = f"/v2/models/{model_name}/versions/{model_version}/generate"

    response = await rest_client.post(endpoint, json=generate_request.dict())
    assert response.status_code == 200

    prediction = InferenceResponse.parse_obj(response.json())
    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data.__root__ == ["What is the capital of France?"]


@pytest.mark.parametrize("settings", [lazy_fixture("settings_stream")])
@pytest.mark.parametrize("sum_model", [lazy_fixture("text_stream_model")])
async def test_generate_stream(
    rest_client: AsyncClient,
    generate_request: InferenceRequest,
    text_stream_model: MLModel,
):
    endpoint = f"/v2/models/{text_stream_model.name}/generate_stream"
    conn = aconnect_sse(rest_client, "POST", endpoint, json=generate_request.dict())
    ref_text = ["What", " is", " the", " capital", " of", " France?"]

    async with conn as stream:
        i = 0
        async for response in stream.aiter_sse():
            prediction = InferenceResponse.parse_obj(response.json())
            assert len(prediction.outputs) == 1
            assert prediction.outputs[0].data.__root__ == [ref_text[i]]
            i += 1


async def test_infer_headers(
    rest_client: AsyncClient,
    inference_request: InferenceRequest,
    sum_model_settings: ModelSettings,
):
    endpoint = f"/v2/models/{sum_model_settings.name}/infer"
    response = await rest_client.post(
        endpoint, json=inference_request.model_dump(), headers={"x-foo": "bar"}
    )

    assert response.status_code == 200
    assert "x-foo" in response.headers
    assert response.headers["x-foo"] == "bar"

    assert CLOUDEVENTS_HEADER_SPECVERSION in response.headers
    assert (
        response.headers[CLOUDEVENTS_HEADER_SPECVERSION]
        == CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT
    )


async def test_infer_error(
    rest_client: AsyncClient, inference_request: InferenceRequest
):
    endpoint = "/v2/models/my-model/versions/v0/infer"
    response = await rest_client.post(endpoint, json=inference_request.model_dump())

    assert response.status_code == 404
    assert response.json()["error"] == "Model my-model with version v0 not found"


async def test_model_repository_index(
    rest_client: AsyncClient, repository_index_request: RepositoryIndexRequest
):
    endpoint = "/v2/repository/index"
    response = await rest_client.post(
        endpoint, json=repository_index_request.model_dump()
    )

    assert response.status_code == 200

    models = response.json()
    assert len(models) == 1


async def test_model_repository_unload(
    rest_client: AsyncClient, sum_model_settings: ModelSettings
):
    endpoint = f"/v2/repository/models/{sum_model_settings.name}/unload"
    response = await rest_client.post(endpoint)

    assert response.status_code == 200

    model_metadata = await rest_client.get(f"/v2/models/{sum_model_settings.name}")
    assert model_metadata.status_code == 404


async def test_model_repository_load(
    rest_client: AsyncClient,
    sum_model_settings: ModelSettings,
):
    await rest_client.post(f"/v2/repository/models/{sum_model_settings.name}/unload")

    endpoint = f"/v2/repository/models/{sum_model_settings.name}/load"
    response = await rest_client.post(endpoint)

    assert response.status_code == 200

    model_metadata = await rest_client.get(f"/v2/models/{sum_model_settings.name}")
    assert model_metadata.status_code == 200


async def test_model_repository_load_error(
    rest_client: AsyncClient, sum_model_settings: ModelSettings
):
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
