import pytest

from mlserver import ModelSettings
from mlserver.types import (
    MetadataTensor,
    MetadataModelErrorResponse,
    InferenceErrorResponse,
)

from .models import SumModel


@pytest.mark.parametrize("ready", [True, False])
def test_ready(data_plane, model_repository, ready):
    model_settings = ModelSettings(name="sum-model-2", version="v1.2.3")
    new_model = SumModel(model_settings)
    model_repository.load(new_model)

    new_model.ready = ready

    all_ready = data_plane.ready()

    assert all_ready == ready


@pytest.mark.parametrize("ready", [True, False])
def test_model_ready(data_plane, sum_model, ready):
    sum_model.ready = ready
    model_ready = data_plane.model_ready(sum_model.name, sum_model.version)

    assert model_ready == ready


@pytest.mark.parametrize(
    "server_name,server_version,extensions",
    [(None, None, None), ("my-server", "v2", ["foo", "bar"])],
)
def test_metadata(settings, data_plane, server_name, server_version, extensions):
    if server_name is not None:
        settings.server_name = server_name

    if server_version is not None:
        settings.server_version = server_version

    if extensions is not None:
        settings.extensions = extensions

    metadata = data_plane.metadata()

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
def test_model_metadata(sum_model_settings, data_plane, platform, versions, inputs):
    if platform is not None:
        sum_model_settings.platform = platform

    if versions is not None:
        sum_model_settings.versions = versions

    if inputs is not None:
        sum_model_settings.inputs = inputs

    metadata = data_plane.model_metadata(
        name=sum_model_settings.name, version=sum_model_settings.version
    )

    assert metadata.name == sum_model_settings.name
    assert metadata.platform == sum_model_settings.platform
    assert metadata.versions == sum_model_settings.versions
    assert metadata.inputs == sum_model_settings.inputs


def test_model_metadata_not_found(data_plane):
    err = data_plane.model_metadata(name="my-model", version="v0")

    assert type(err) == MetadataModelErrorResponse
    assert err.error == "Model my-model with version v0 not found"


def test_infer(data_plane, sum_model, inference_request):
    prediction = data_plane.infer(sum_model.name, sum_model.version, inference_request)

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == [21]


def test_infer_not_found(data_plane, inference_request):
    err = data_plane.infer("my-model", "v0", inference_request)

    assert type(err) == InferenceErrorResponse
    assert err.error == "Model my-model with version v0 not found"
