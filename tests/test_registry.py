import pytest
import asyncio

from asyncio import CancelledError
from typing import List, Union

from mlserver.model import MLModel
from mlserver.errors import MLServerError, ModelNotFound
from mlserver.registry import MultiModelRegistry, SingleModelRegistry
from mlserver.settings import ModelSettings, ModelParameters

from .fixtures import ErrorModel, SlowModel


@pytest.fixture
async def model_registry(
    model_registry: MultiModelRegistry, mocker
) -> MultiModelRegistry:
    async def _async_val(model: MLModel, new_model: MLModel = None) -> MLModel:
        if new_model:
            return new_model

        return model

    load_stub = mocker.stub("_on_model_load")
    load_stub.side_effect = _async_val
    model_registry._on_model_load = [load_stub]

    reload_stub = mocker.stub("_on_model_reload")
    reload_stub.side_effect = _async_val
    model_registry._on_model_reload = [reload_stub]

    unload_stub = mocker.stub("_on_model_unload")
    unload_stub.side_effect = _async_val
    model_registry._on_model_unload = [unload_stub]

    for single_registry in model_registry._models.values():
        single_registry._on_model_load = [load_stub]
        single_registry._on_model_reload = [reload_stub]
        single_registry._on_model_unload = [unload_stub]

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
        assert str(err.value) == f"Model {name} with version {version} not found"
    else:
        assert str(err.value) == f"Model {name} not found"


@pytest.mark.parametrize(
    "name, version",
    [("sum-model", "v1.2.3"), ("sum-model", None), ("sum-model", "")],
)
async def test_get_model(model_registry, sum_model, name, version):
    found_model = await model_registry.get_model(name, version)
    assert found_model.ready
    assert found_model == sum_model


async def test_model_hooks(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    sum_model_settings.name = "sum-model-2"

    sum_model = await model_registry.load(sum_model_settings)
    assert sum_model.ready

    for callback in model_registry._on_model_load:
        callback.assert_called_once_with(sum_model)

    await model_registry.unload(sum_model.name)
    for callback in model_registry._on_model_unload:
        callback.assert_called_once_with(sum_model)


async def test_reload_model(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    existing_model = await model_registry.get_model(sum_model_settings.name)
    new_model = await model_registry.load(sum_model_settings)

    reloaded_model = await model_registry.get_model(sum_model_settings.name)
    assert new_model != existing_model
    assert new_model == reloaded_model
    assert reloaded_model.ready

    for callback in model_registry._on_model_load:
        callback.assert_not_called()

    for callback in model_registry._on_model_reload:
        callback.assert_called_once_with(existing_model, new_model)

    for callback in model_registry._on_model_unload:
        callback.assert_not_called()


async def test_load_multi_version(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    existing_model = await model_registry.get_model(sum_model_settings.name)
    existing_version = sum_model_settings.parameters.version

    # Load new model
    new_model_settings = sum_model_settings.copy(deep=True)
    new_model_settings.parameters.version = "v2.0.0"
    new_model = await model_registry.load(new_model_settings)
    assert new_model.ready

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


@pytest.mark.parametrize(
    "versions, expected",
    [
        (["4", "3", "2", "1", "7", "5", "6"], "7"),
        (["v1", "v3", "v2"], "v3"),
        (["v10", "v3", "v2"], "v3"),
        (["8", "v3", "7"], "v3"),
        (["v1.0.0", "v1.2.3", "v12.3.4"], "v12.3.4"),
    ],
)
async def test_find_default(
    versions: List[str],
    expected: str,
    sum_model_settings: ModelSettings,
):
    model_settings = sum_model_settings.copy(deep=True)
    model_settings.name = "model-foo"
    foo_registry = SingleModelRegistry(model_settings)

    # Load mock models
    for version in versions:
        model_settings = model_settings.copy(deep=True)
        model_settings.parameters.version = version
        await foo_registry.load(model_settings)

    foo_registry._clear_default()
    default_model = foo_registry._find_default()
    assert default_model.version == expected


async def test_model_not_ready(model_registry: MultiModelRegistry):
    slow_model_settings = ModelSettings(name="slow-model", implementation=SlowModel)

    load_task = asyncio.create_task(model_registry.load(slow_model_settings))
    # Use asyncio.sleep() to give control back to loop so that the load above
    # gets executed
    await asyncio.sleep(0.1)

    models = list(await model_registry.get_models())
    assert not all([m.ready for m in models])
    assert len(models) == 2

    # Cancel slow load task
    load_task.cancel()
    try:
        await load_task
    except CancelledError:
        pass


async def test_model_load_error(model_registry: MultiModelRegistry):
    error_model_settings = ModelSettings(
        name="error-model",
        implementation=ErrorModel,
        parameters=ModelParameters(load_error=True),
    )

    with pytest.raises(MLServerError):
        await model_registry.load(error_model_settings)

    with pytest.raises(ModelNotFound):
        await model_registry.get_model(error_model_settings.name)

    models = list(await model_registry.get_models())
    assert len(models) == 1


async def test_rolling_reload(
    model_registry: MultiModelRegistry, sum_model_settings: ModelSettings
):
    sum_model_settings.implementation = SlowModel
    reload_task = asyncio.create_task(model_registry.load(sum_model_settings))
    # Use asyncio.sleep() to give control back to loop so that the load above
    # starts to get executed
    await asyncio.sleep(0.1)

    # Assert that the old model stays ready while the new version is getting loaded
    models = list(await model_registry.get_models())
    assert all([m.ready for m in models])
    assert len(models) == 1

    # Cancel slow reload task
    reload_task.cancel()
    try:
        await reload_task
    except CancelledError:
        pass
