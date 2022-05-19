import asyncio
import signal

from typing import List

from .model import MLModel
from .settings import Settings, ModelSettings
from .logging import configure_logger
from .registry import MultiModelRegistry
from .repository import ModelRepository
from .handlers import DataPlane, ModelRepositoryHandlers
from .parallel import InferencePool
from .batching import load_batching
from .rest import RESTServer
from .grpc import GRPCServer

HANDLED_SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]


class MLServer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._inference_pool = None
        on_model_load = [
            self.add_custom_handlers,
            load_batching,
        ]
        on_model_reload = [self.reload_custom_handlers]
        on_model_unload = [self.remove_custom_handlers]

        if self._settings.parallel_workers:
            # Only load inference pool if parallel inference has been enabled
            self._inference_pool = InferencePool(self._settings)
            on_model_load = [
                self.add_custom_handlers,
                self._inference_pool.load_model,
                load_batching,
            ]
            on_model_reload = [
                self.reload_custom_handlers,
                self._inference_pool.reload_model,  # type: ignore
            ]
            on_model_unload = [
                self.remove_custom_handlers,
                self._inference_pool.unload_model,  # type: ignore
            ]

        self._model_registry = MultiModelRegistry(
            on_model_load=on_model_load,  # type: ignore
            on_model_reload=on_model_reload,  # type: ignore
            on_model_unload=on_model_unload,  # type: ignore
        )
        self._model_repository = ModelRepository(self._settings.model_repository_root)
        self._data_plane = DataPlane(
            settings=self._settings, model_registry=self._model_registry
        )
        self._model_repository_handlers = ModelRepositoryHandlers(
            repository=self._model_repository, model_registry=self._model_registry
        )

        self._logger = configure_logger(settings)

        self._rest_server = RESTServer(
            self._settings, self._data_plane, self._model_repository_handlers
        )
        self._grpc_server = GRPCServer(
            self._settings, self._data_plane, self._model_repository_handlers
        )

    async def start(self, models_settings: List[ModelSettings] = []):
        self._add_signal_handlers()

        servers_task = asyncio.gather(
            self._rest_server.start(), self._grpc_server.start()
        )

        await asyncio.gather(
            *[
                self._model_registry.load(model_settings)
                for model_settings in models_settings
            ]
        )

        await servers_task

    async def add_custom_handlers(self, model: MLModel):
        await self._rest_server.add_custom_handlers(model)

        # TODO: Add support for custom gRPC endpoints
        # self._grpc_server.add_custom_handlers(handlers)

    async def reload_custom_handlers(self, old_model: MLModel, new_model: MLModel):
        await self.add_custom_handlers(new_model)
        await self.remove_custom_handlers(old_model)

        # TODO: Add support for custom gRPC endpoints
        # self._grpc_server.delete_custom_handlers(handlers)

    async def remove_custom_handlers(self, model: MLModel):
        await self._rest_server.delete_custom_handlers(model)

        # TODO: Add support for custom gRPC endpoints
        # self._grpc_server.delete_custom_handlers(handlers)

    def _add_signal_handlers(self):
        loop = asyncio.get_event_loop()

        for sign in HANDLED_SIGNALS:
            loop.add_signal_handler(sign, lambda: asyncio.create_task(self.stop()))

    async def stop(self):
        await self._rest_server.stop()
        await self._grpc_server.stop()
        if self._inference_pool:
            await self._inference_pool.close()
