import pytest

from mlserver.errors import ModelNotFound
from mlserver.model import MLModel
from mlserver.registry import MultiModelRegistry
from mlserver.settings import ModelSettings


@pytest.fixture
def model_registry(model_registry: MultiModelRegistry, mocker) -> MultiModelRegistry:
    async def _async_val():
        return None

    for single_registry in model_registry._models.values():
        single_registry._on_model_load = [mocker.stub("_on_model_load")]
        single_registry._on_model_load[0].return_value = _async_val()

        single_registry._on_model_unload = [mocker.stub("_on_model_unload")]
        single_registry._on_model_unload[0].return_value = _async_val()

    return model_registry


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
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    sum_model_settings.name = "sum-model-2"

    sum_model = await model_registry.load(sum_model_settings)
    for callback in model_registry._on_model_load:
        callback.assert_called_once_with(sum_model)

    await model_registry.unload(sum_model.name)
    for callback in model_registry._on_model_unload:
        callback.assert_called_once_with(sum_model)


async def test_load_refresh(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    existing_model = await model_registry.get_model(sum_model_settings.name)
    new_model = await model_registry.load(sum_model_settings)

    reloaded_model = await model_registry.get_model(sum_model_settings.name)
    assert new_model != existing_model
    assert new_model == reloaded_model

    for callback in model_registry._on_model_load:
        callback.assert_called_once_with(new_model)

    for callback in model_registry._on_model_unload:
        callback.assert_called_once_with(existing_model)


async def test_load_multi_version(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    existing_model = await model_registry.get_model(sum_model_settings.name)
    existing_version = sum_model_settings.parameters.version

    # Load new model
    sum_model_settings.parameters.version = "v2.0.0"
    new_model = await model_registry.load(sum_model_settings)

    # Ensure latest model is now the default one
    default_model = await model_registry.get_model(sum_model_settings.name)
    assert new_model != existing_model
    assert new_model == default_model

    for callback in model_registry._on_model_load:
        callback.assert_called_once_with(new_model)

    # Ensure old model is still reachable
    old_model = await model_registry.get_model(
        sum_model_settings.name, existing_version
    )
    assert old_model == existing_model

    for callback in model_registry._on_model_unload:
        callback.assert_not_called_with(existing_model)
