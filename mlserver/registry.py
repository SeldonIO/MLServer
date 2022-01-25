import asyncio

from typing import Callable, Coroutine, List, Dict, Optional
from itertools import chain
from functools import cmp_to_key

from .model import MLModel
from .errors import ModelNotFound
from .types import RepositoryIndexResponse
from .logging import logger
from .settings import ModelSettings

ModelRegistryHook = Callable[[MLModel], Coroutine[None, None, None]]


def _get_version(model_settings: ModelSettings) -> Optional[str]:
    if model_settings.parameters:
        return model_settings.parameters.version

    return None


def _is_newer(a: MLModel, b: MLModel) -> int:
    """
    Returns true if 'a' is newer than 'b'.

    TODO: Support other ordering schemes (e.g. semver).
    """
    if a.version is None:
        return 1

    if b.version is None:
        return -1

    try:
        a_int = int(a.version)
        b_int = int(b.version)

        return a_int - b_int
    except ValueError:
        if a.version > b.version:
            return 1
        elif a.version < b.version:
            return -1
        else:
            return 0


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
        self._default: Optional[MLModel] = None

        self._name = model_settings.name
        self._on_model_load = on_model_load
        self._on_model_unload = on_model_unload

    @property
    def default(self) -> Optional[MLModel]:
        if self._default is None:
            self._default = self._find_default()

        return self._default

    def _find_default(self) -> Optional[MLModel]:
        if self._default is None:
            if self._versions:
                version_key = cmp_to_key(_is_newer)
                latest_model = max(self._versions.values(), key=version_key)
                return latest_model

        return self._default

    def _clear_default(self):
        self._default = None

    def _refresh_default(self, new_model: MLModel = None) -> Optional[MLModel]:
        if new_model:
            # Check whether new model is "defaulter" than current default
            # NOTE: This should help to avoid iterating through all versioned
            # models each time a new model is loaded to find the latest

            if self._default is None:
                # If default is currently empty, take new one as new default
                self._default = new_model
                return new_model

            if new_model.version is None:
                # If new model doesn't have a version, assume it's "defaulter"
                # than previous default
                self._default = new_model
                return new_model

            if self._default.version is None:
                # If default doesn't have a version (and new one does), assume
                # that current default is "defaulter" than new one
                return self._default

            # Otherwise, compare versions
            if _is_newer(new_model, self._default) >= 0:
                self._default = new_model
                return new_model

            return self._default

        if self._default and self._default.version is None:
            # If there isn't a new model to compare, and current default has no
            # version, then consider that current one is "defaulter" than other
            # versioned models
            return self._default

        # Otherwise, find latest from current set of versions
        self._default = self._find_default()
        return self._default

    async def index(self) -> RepositoryIndexResponse:
        pass

    async def load(self, model_settings: ModelSettings) -> MLModel:
        # If there's a previously loaded model, we'll need to unload it at the
        # end
        previous_version = _get_version(model_settings)
        previous_loaded_model = self._find_model(previous_version)

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
        self._clear_default()

    async def unload_version(self, version: str = None):
        if version:
            model = await self.get_model(version)
            await self._unload_model(model)
            del self._versions[version]

            if model == self.default:
                self._clear_default()

        elif self.default and not self.default.version:
            # If version is None, and default model doesn't have a version,
            # then unload and find a new default
            await self._unload_model(self.default)
            self._clear_default()

    async def _unload_model(self, model: MLModel):
        if self._on_model_unload:
            await asyncio.gather(
                *[callback(model) for callback in self._on_model_unload]
            )

        if model == self.default:
            self._clear_default()

        logger.info(f"Unloaded model '{model.name}' succesfully.")

    def _find_model(self, version: str = None) -> Optional[MLModel]:
        if version:
            if version not in self._versions:
                return None

            return self._versions[version]

        return self.default

    async def get_model(self, version: str = None) -> MLModel:
        model = self._find_model(version)

        if model is None:
            raise ModelNotFound(self._name, version)

        return model

    async def get_models(self) -> List[MLModel]:
        # NOTE: `.values()` returns a "view" instead of a list
        models = list(self._versions.values())

        # Add default if not versioned (as it won't be present on the
        # `_versions` dict
        if self.default and not self.default.version:
            models.append(self.default)

        return models

    def _register(self, model: MLModel):
        if model.version:
            self._versions[model.version] = model

        self._refresh_default(model)

    def empty(self) -> bool:
        if self._versions:
            return False

        return self.default is None


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
        model_registry = self._get_model_registry(name)
        await model_registry.unload()
        del self._models[name]

    async def unload_version(self, name: str, version: str = None):
        model_registry = self._get_model_registry(name, version)
        await model_registry.unload_version(version)
        if model_registry.empty():
            del self._models[name]

    async def get_model(self, name: str, version: str = None) -> MLModel:
        model_registry = self._get_model_registry(name, version)
        return await model_registry.get_model(version)

    async def get_models(self, name: str = None) -> List[MLModel]:
        if name is not None:
            model_registry = self._get_model_registry(name)
            return await model_registry.get_models()

        models_list = await asyncio.gather(
            *[model.get_models() for model in self._models.values()]
        )

        return chain.from_iterable(models_list)  # type: ignore

    def _get_model_registry(
        self, name: str, version: str = None
    ) -> SingleModelRegistry:
        if name not in self._models:
            raise ModelNotFound(name, version)

        return self._models[name]
