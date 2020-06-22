import pytest

from .models import SumModel


@pytest.mark.parametrize("ready", [True, False])
def test_ready(data_plane, model_registry, ready):
    new_model = SumModel("sum-model-2", "1.2.3")
    model_registry.load(model_name=new_model.name, model=new_model)

    new_model.ready = ready

    all_ready = data_plane.ready()

    assert all_ready == ready


@pytest.mark.parametrize("ready", [True, False])
def test_model_ready(data_plane, sum_model, ready):
    sum_model.ready = ready
    model_ready = data_plane.model_ready(sum_model.name)

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


def test_infer(data_plane, sum_model, inference_request):
    prediction = data_plane.infer(sum_model.name, inference_request)

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].data == [21]
