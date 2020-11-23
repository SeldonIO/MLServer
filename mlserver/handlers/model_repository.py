from ..settings import ModelSettings
from ..registry import MultiModelRegistry
from ..repository import ModelRepository
from ..types import (
    RepositoryIndexRequest,
    RepositoryIndexResponse,
    RepositoryIndexResponseItem,
)


class ModelRepositoryHandlers:
    def __init__(self, repository: ModelRepository, model_registry: MultiModelRegistry):
        self._repository = repository
        self._model_registry = model_registry

    async def index(self, payload: RepositoryIndexRequest) -> RepositoryIndexResponse:
        # TODO: Filter by payload.ready flag
        all_model_settings = await self._repository.list()
        repository_items = [
            self._to_item(model_settings) for model_settings in all_model_settings
        ]

        return RepositoryIndexResponse(__root__=repository_items)

    def _to_item(self, model_settings: ModelSettings) -> RepositoryIndexResponseItem:
        item = RepositoryIndexResponseItem(
            name=model_settings.name,
            # TODO: Set a valid state and reason
            # https://github.com/triton-inference-server/server/blob/a95889414eae2d29073debecf2cce82dac6c2589/src/core/model_repository_manager.cc#L59-L87
            state="",
            reason="",
        )

        if model_settings.parameters:
            item.version = model_settings.parameters.version

        return item

    async def load(self, name: str) -> bool:
        model_settings = await self._repository.find(name)

        # TODO: Move to separate method
        model_class = model_settings.implementation
        model = model_class(model_settings)

        await self._model_registry.load(model)

        return True

    async def unload(self, name: str) -> bool:
        await self._model_registry.unload(name)

        return True
