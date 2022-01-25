import pytest

from typing import Optional

from mlserver.errors import ModelNotFound
from mlserver.registry import MultiModelRegistry
from mlserver.handlers import ModelRepositoryHandlers
from mlserver.settings import ModelSettings
from mlserver.types import RepositoryIndexRequest, State


async def test_index(
    model_repository_handlers: ModelRepositoryHandlers,
    repository_index_request: RepositoryIndexRequest,
    sum_model_settings: ModelSettings,
):
    repo_index = list(await model_repository_handlers.index(repository_index_request))

    assert len(repo_index) == 1
    assert repo_index[0].name == sum_model_settings.name
    assert (
        repo_index[0].version == sum_model_settings.parameters.version  # type: ignore
    )
    assert repo_index[0].state == State.READY


async def test_index_unavailable_model(
    model_repository_handlers: ModelRepositoryHandlers,
    repository_index_request: RepositoryIndexRequest,
    sum_model_settings: ModelSettings,
):
    await model_repository_handlers.unload(sum_model_settings.name)
    repo_index = list(await model_repository_handlers.index(repository_index_request))

    assert len(repo_index) == 1
    assert repo_index[0].name == sum_model_settings.name
    assert (
        repo_index[0].version == sum_model_settings.parameters.version  # type: ignore
    )
    assert repo_index[0].state == State.UNAVAILABLE


@pytest.mark.parametrize("ready,expected", [(None, 1), (True, 0), (False, 1)])
async def test_index_filter_ready(
    model_repository_handlers: ModelRepositoryHandlers,
    repository_index_request: RepositoryIndexRequest,
    sum_model_settings: ModelSettings,
    ready: Optional[bool],
    expected: int,
):
    await model_repository_handlers.unload(sum_model_settings.name)

    repository_index_request.ready = ready
    repo_index = list(await model_repository_handlers.index(repository_index_request))

    assert len(repo_index) == expected


async def test_unload(
    model_repository_handlers: ModelRepositoryHandlers,
    model_registry: MultiModelRegistry,
    sum_model_settings: ModelSettings,
):
    await model_repository_handlers.unload(sum_model_settings.name)

    with pytest.raises(ModelNotFound):
        await model_registry.get_model(sum_model_settings.name)


async def test_unload_not_found(
    model_repository_handlers: ModelRepositoryHandlers,
):
    with pytest.raises(ModelNotFound):
        await model_repository_handlers.unload("not-existing")


async def test_load_not_found(
    model_repository_handlers: ModelRepositoryHandlers,
):
    with pytest.raises(ModelNotFound):
        await model_repository_handlers.load("not-existing")


async def test_load_removes_stale_models(
    model_repository_handlers: ModelRepositoryHandlers,
    repository_index_request: RepositoryIndexRequest,
    model_registry: MultiModelRegistry,
    sum_model_settings: ModelSettings,
):
    # Load a few models which are not present on the repository (including a
    # default one), therefore they will be stale
    stale_settings = sum_model_settings.copy(deep=True)
    stale_settings.parameters.version = None
    await model_registry.load(stale_settings)

    to_load = ["v0", "v1", "v2"]
    for version in to_load:
        stale_settings = sum_model_settings.copy(deep=True)
        stale_settings.parameters.version = version
        await model_registry.load(stale_settings)

    # Validate that the stale test models have been loaded
    registry_models = await model_registry.get_models(sum_model_settings.name)
    stale_length = (
        len(to_load)
        + 1  # Count the (stale) default model
        + 1  # Count the previous (non-stale) model
    )
    assert len(registry_models) == stale_length

    # Reload our model and validate whether stale models have been removed
    await model_repository_handlers.load(sum_model_settings.name)

    # Assert that stale models have been removed from both the registry (and
    # ensure they are not present on the repository either)
    registry_models = await model_registry.get_models(sum_model_settings.name)
    repo_models = list(await model_repository_handlers.index(repository_index_request))
    expected_version = sum_model_settings.parameters.version

    assert len(registry_models) == 1
    assert registry_models[0].version == expected_version

    assert len(repo_models) == 1
    assert repo_models[0].version == expected_version
