from mlserver.handlers import ModelRepositoryHandlers
from mlserver.settings import ModelSettings


async def test_index(
    model_repository_handlers: ModelRepositoryHandlers,
    sum_model_settings: ModelSettings,
):
    repo_index = list(await model_repository_handlers.index())

    assert len(repo_index) == 1
    assert repo_index[0].name == sum_model_settings.name
    assert repo_index[0].version == sum_model_settings.parameters.version
