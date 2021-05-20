import pytest
import uuid

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import MetadataTensor

from ..fixtures import SumModel


@pytest.mark.parametrize("ready", [True, False])
async def test_ready(data_plane, model_registry, ready):
    model_settings = ModelSettings(
        name="sum-model-2", parameters=ModelParameters(version="v1.2.3")
    )
    new_model = SumModel(model_settings)
    await model_registry.load(new_model)

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
    assert prediction.outputs[0].data.__root__ == [21]


async def test_infer_generates_uuid(data_plane, sum_model, inference_request):
    inference_request.id = None
    prediction = await data_plane.infer(
        payload=inference_request, name=sum_model.name, version=sum_model.version
    )

    assert prediction.id is not None
    assert prediction.id == str(uuid.UUID(prediction.id))
