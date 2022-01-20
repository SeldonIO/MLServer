import asyncio

from typing import Callable, Coroutine, List, Dict, Optional
from itertools import chain

from .model import MLModel
from .errors import ModelNotFound
from .types import RepositoryIndexResponse
from .logging import logger
from .settings import ModelSettings

ModelRegistryHook = Callable[[MLModel], Coroutine[None, None, None]]


class SingleModelRegistry:
    """
    Registry for a single model with multiple versions.
    """

    def __init__(
        self,
        model_settings: ModelSettings,
        on_model_load: List[ModelRegistryHook] = [],
        on_model_unload: List[ModelRegistryHook] = [],
    ):
        self._versions: Dict[str, MLModel] = {}

        self._name = model_settings.name
        self._on_model_load = on_model_load
        self._on_model_unload = on_model_unload

    async def index(self) -> RepositoryIndexResponse:
        pass

    async def load(self, model_settings: ModelSettings) -> MLModel:
        # If there's a previously loaded model, we'll need to unload it at the
        # end
        previous_loaded_model = await self._find_model(model_settings)

        model_class = model_settings.implementation
        new_model = model_class(model_settings)  # type: ignore

        await self._load_model(new_model)

        if previous_loaded_model:
            await self._unload_model(previous_loaded_model)

        logger.info(f"Loaded model '{new_model.name}' succesfully.")
        return new_model

    async def _load_model(self, model: MLModel):
        await model.load()
        self._register(model)

        if self._on_model_load:
            # TODO: Expose custom handlers on ParallelRuntime
            await asyncio.gather(*[callback(model) for callback in self._on_model_load])

    async def unload(self):
        models = await self.get_models()
        await asyncio.gather(*[self._unload_model(model) for model in models])

        self._versions.clear()
        self._default = None

    async def _unload_model(self, model: MLModel):
        if self._on_model_unload:
            await asyncio.gather(
                *[callback(model) for callback in self._on_model_unload]
            )

        logger.info(f"Unloaded model '{model.name}' succesfully.")

    async def _find_model(self, model_settings: ModelSettings) -> Optional[MLModel]:
        version = None
        if model_settings.parameters and model_settings.parameters.version:
            version = model_settings.parameters.version

        try:
            return await self.get_model(version)
        except ModelNotFound:
            return None

    async def get_model(self, version: str = None) -> MLModel:
        if version:
            if version not in self._versions:
                raise ModelNotFound(self._name, version)

            return self._versions[version]

        return self._default

    async def get_models(self) -> List[MLModel]:
        # NOTE: `.values()` returns a "view" instead of a list
        models = list(self._versions.values())

        # Add default if not versioned
        if not self._default.version:
            models.append(self._default)

        return models

    def _register(self, model: MLModel):
        if model.version:
            self._versions[model.version] = model

        # TODO: Support version policies
        self._default = model


class MultiModelRegistry:
    """
    Multiple model registry, where each model can have multiple versions.
    """

    def __init__(
        self,
        on_model_load: List[ModelRegistryHook] = [],
        on_model_unload: List[ModelRegistryHook] = [],
    ):
        self._models: Dict[str, SingleModelRegistry] = {}
        self._on_model_load = on_model_load
        self._on_model_unload = on_model_unload

    async def load(self, model_settings: ModelSettings) -> MLModel:
        if model_settings.name not in self._models:
            self._models[model_settings.name] = SingleModelRegistry(
                model_settings,
                on_model_load=self._on_model_load,
                on_model_unload=self._on_model_unload,
            )

        return await self._models[model_settings.name].load(model_settings)

    async def unload(self, name: str):
        if name not in self._models:
            raise ModelNotFound(name)

        await self._models[name].unload()
        del self._models[name]

    async def get_model(self, name: str, version: str = None) -> MLModel:
        if name not in self._models:
            raise ModelNotFound(name, version)

        return await self._models[name].get_model(version)

    async def get_models(self) -> List[MLModel]:
        models_list = await asyncio.gather(
            *[model.get_models() for model in self._models.values()]
        )

        return chain.from_iterable(models_list)  # type: ignore
