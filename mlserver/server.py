import asyncio
import signal

from typing import List

from .model import MLModel
from .settings import Settings
from .registry import MultiModelRegistry
from .repository import ModelRepository
from .handlers import DataPlane, ModelRepositoryHandlers
from .parallel import load_inference_pool, unload_inference_pool
from .rest import RESTServer
from .grpc import GRPCServer

HANDLED_SIGNALS = [signal.SIGINT, signal.SIGTERM]


class MLServer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._model_registry = MultiModelRegistry(
            on_model_load=[self.add_custom_handlers, load_inference_pool],
            on_model_unload=[self.remove_custom_handlers, unload_inference_pool],
        )
        self._model_repository = ModelRepository(self._settings.model_repository_root)
        self._data_plane = DataPlane(
            settings=self._settings, model_registry=self._model_registry
        )
        self._model_repository_handlers = ModelRepositoryHandlers(
            repository=self._model_repository, model_registry=self._model_registry
        )

    async def start(self, models: List[MLModel] = []):
        self._add_signal_handlers()

        self._rest_server = RESTServer(
            self._settings, self._data_plane, self._model_repository_handlers
        )
        self._grpc_server = GRPCServer(
            self._settings, self._data_plane, self._model_repository_handlers
        )

        # TODO: Discover models from ModelRepository
        # TODO: Add flag to disable autoload of models
        load_tasks = [self._model_registry.load(model) for model in models]
        await asyncio.gather(*load_tasks)

        await asyncio.gather(self._rest_server.start(), self._grpc_server.start())

    async def add_custom_handlers(self, model: MLModel):
        await self._rest_server.add_custom_handlers(model)

        # TODO: Add support for custom gRPC endpoints
        # self._grpc_server.add_custom_handlers(handlers)

    async def remove_custom_handlers(self, model: MLModel):
        await self._rest_server.delete_custom_handlers(model)

        # TODO: Add support for custom gRPC endpoints
        # self._grpc_server.delete_custom_handlers(handlers)

    def _add_signal_handlers(self):
        loop = asyncio.get_event_loop()

        for sign in HANDLED_SIGNALS:
            loop.add_signal_handler(sign, lambda: asyncio.ensure_future(self.stop()))

    async def stop(self):
        await self._rest_server.stop()
        await self._grpc_server.stop()
