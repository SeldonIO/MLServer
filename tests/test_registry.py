import pytest

from mlserver.errors import ModelNotFound
from mlserver.model import MLModel
from mlserver.registry import MultiModelRegistry


@pytest.mark.parametrize(
    "name, version",
    [
        ("sum-model", "v0"),
        ("sum-model-2", "v0"),
        ("sum-model", "v2"),
        ("sum-model-2", None),
    ],
)
async def test_get_model_not_found(model_registry, name, version):
    with pytest.raises(ModelNotFound) as err:
        await model_registry.get_model(name, version)

        if version is not None:
            assert err.message == f"Model {name} with version {version} not found"
        else:
            assert err.message == f"Model {name} not found"


@pytest.mark.parametrize(
    "name, version",
    [("sum-model", "v1.2.3"), ("sum-model", None), ("sum-model", "")],
)
async def test_get_model(model_registry, sum_model, name, version):
    found_model = await model_registry.get_model(name, version)
    assert found_model == sum_model


async def test_model_hooks(
    model_registry: MultiModelRegistry, sum_model: MLModel, mocker
):
    sum_model._settings.name = "sum-model-2"

    async def _async_val():
        return None

    model_registry._on_model_load = [mocker.stub("_on_model_load")]
    model_registry._on_model_load[0].return_value = _async_val()

    model_registry._on_model_unload = [mocker.stub("_on_model_unload")]
    model_registry._on_model_unload[0].return_value = _async_val()

    await model_registry.load(sum_model)
    for callback in model_registry._on_model_load:
        callback.assert_called_once_with(sum_model)

    await model_registry.unload(sum_model.name)
    for callback in model_registry._on_model_unload:
        callback.assert_called_once_with(sum_model)
