import pytest
import uuid

from mlserver.errors import ModelNotReady
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import MetadataTensor, InferenceResponse, TensorData

from ..fixtures import SumModel


@pytest.mark.parametrize("ready", [True, False])
async def test_ready(data_plane, model_registry, ready):
    model_settings = ModelSettings(
        name="sum-model-2",
        parameters=ModelParameters(version="v1.2.3"),
        implementation=SumModel,
    )
    new_model = await model_registry.load(model_settings)

    new_model.ready = ready

    all_ready = await data_plane.ready()

    assert all_ready == ready


@pytest.mark.parametrize("ready", [True, False])
async def test_model_ready(data_plane, sum_model, ready):
    sum_model.ready = ready
    model_ready = await data_plane.model_ready(sum_model.name, sum_model.version)

    assert model_ready == ready


@pytest.mark.parametrize(
    "server_name,server_version,extensions",
    [(None, None, None), ("my-server", "v2", ["foo", "bar"])],
)
async def test_metadata(settings, data_plane, server_name, server_version, extensions):
    if server_name is not None:
        settings.server_name = server_name

    if server_version is not None:
        settings.server_version = server_version

    if extensions is not None:
        settings.extensions = extensions

    metadata = await data_plane.metadata()

    assert metadata.name == settings.server_name
    assert metadata.version == settings.server_version
    assert metadata.extensions == settings.extensions


@pytest.mark.parametrize(
    "platform,versions,inputs",
    [
        (None, None, None),
        ("sklearn", ["sklearn/0.22.3"], None),
        (
            "xgboost",
            ["xgboost/1.1.0"],
            [MetadataTensor(name="input-0", datatype="FP32", shape=[6, 7])],
        ),
    ],
)
async def test_model_metadata(
    sum_model_settings, data_plane, platform, versions, inputs
):
    if platform is not None:
        sum_model_settings.platform = platform

    if versions is not None:
        sum_model_settings.versions = versions

    if inputs is not None:
        sum_model_settings.inputs = inputs

    metadata = await data_plane.model_metadata(
        name=sum_model_settings.name, version=sum_model_settings.parameters.version
    )

    assert metadata.name == sum_model_settings.name
    assert metadata.platform == sum_model_settings.platform
    assert metadata.versions == sum_model_settings.versions
    assert metadata.inputs == sum_model_settings.inputs


async def test_infer(data_plane, sum_model, inference_request):
    prediction = await data_plane.infer(
        payload=inference_request, name=sum_model.name, version=sum_model.version
    )

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == TensorData(root=[6])


async def test_infer_error_not_ready(data_plane, sum_model, inference_request):
    sum_model.ready = False
    with pytest.raises(ModelNotReady):
        await data_plane.infer(payload=inference_request, name=sum_model.name)

    sum_model.ready = True
    prediction = await data_plane.infer(payload=inference_request, name=sum_model.name)
    assert len(prediction.outputs) == 1


async def test_infer_generates_uuid(data_plane, sum_model, inference_request):
    inference_request.id = None
    prediction = await data_plane.infer(
        payload=inference_request, name=sum_model.name, version=sum_model.version
    )

    assert prediction.id is not None
    assert prediction.id == str(uuid.UUID(prediction.id))


async def test_infer_response_cache(cached_data_plane, sum_model, inference_request):
    cache_key = inference_request.json()
    payload = inference_request.copy(deep=True)
    prediction = await cached_data_plane.infer(
        payload=payload, name=sum_model.name, version=sum_model.version
    )

    response_cache = cached_data_plane._get_response_cache()
    assert response_cache is not None
    assert await response_cache.size() == 1

    cache_value = await response_cache.lookup(cache_key)
    cached_response = InferenceResponse.parse_raw(cache_value)
    assert cached_response.model_name == prediction.model_name
    assert cached_response.model_version == prediction.model_version
    assert cached_response.Config == prediction.Config
    assert cached_response.outputs == prediction.outputs

    prediction = await cached_data_plane.infer(
        payload=inference_request, name=sum_model.name, version=sum_model.version
    )

    # Using existing cache value
    assert await response_cache.size() == 1
    assert cached_response.model_name == prediction.model_name
    assert cached_response.model_version == prediction.model_version
    assert cached_response.Config == prediction.Config
    assert cached_response.outputs == prediction.outputs


async def test_response_cache_disabled(data_plane):
    response_cache = data_plane._get_response_cache()
    assert response_cache is None
