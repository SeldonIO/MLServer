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
