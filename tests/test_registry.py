import pytest

from typing import List, Union

from mlserver.errors import ModelNotFound
from mlserver.registry import MultiModelRegistry
from mlserver.settings import ModelSettings


@pytest.fixture
async def model_registry(
    model_registry: MultiModelRegistry, mocker
) -> MultiModelRegistry:
    async def _async_val():
        return None

    coros = []
    for single_registry in model_registry._models.values():
        load_coro = _async_val()
        single_registry._on_model_load = [mocker.stub("_on_model_load")]
        single_registry._on_model_load[0].return_value = load_coro
        coros.append(load_coro)

        unload_coro = _async_val()
        single_registry._on_model_unload = [mocker.stub("_on_model_unload")]
        single_registry._on_model_unload[0].return_value = unload_coro
        coros.append(unload_coro)

    yield model_registry

    # Remove warning about "coroutine never awaited"
    for coro in coros:
        try:
            await coro
        except RuntimeError:
            pass


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


@pytest.mark.parametrize(
    "versions_to_unload",
    [
        [None],
        [None, "v0"],
        ["v0", None],
        ["v0"],
        ["v0", "v1", "v2"],
        [None, "v0", "v1", "v2"],
        ["v0", "v1", "v2", None],
    ],
)
async def test_unload_version(
    versions_to_unload: List[Union[str, None]],
    model_registry: MultiModelRegistry,
    sum_model_settings: ModelSettings,
):
    # Load multiple versions
    to_load = ["v0", "v1", "v2"]
    sum_model_settings.name = "model-foo"

    sum_model_settings = sum_model_settings.copy(deep=True)
    sum_model_settings.parameters.version = None
    default_model = await model_registry.load(sum_model_settings)
    for version in to_load:
        sum_model_settings = sum_model_settings.copy(deep=True)
        sum_model_settings.parameters.version = version
        await model_registry.load(sum_model_settings)

    # Unload versions
    for version in versions_to_unload:
        await model_registry.unload_version(sum_model_settings.name, version)

    if len(versions_to_unload) == len(to_load) + 1:
        # If we have unloaded all models (including the default one), assert
        # that the model has been completely unloaded
        with pytest.raises(ModelNotFound):
            await model_registry.get_models(sum_model_settings.name)
    else:
        models = await model_registry.get_models(sum_model_settings.name)
        for model in models:
            assert model.version not in versions_to_unload

        if None in versions_to_unload:
            new_default_model = await model_registry.get_model(sum_model_settings.name)
            assert new_default_model != default_model
