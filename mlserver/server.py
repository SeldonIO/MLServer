import asyncio
import signal

from typing import List

from .model import MLModel
from .settings import Settings
from .repository import ModelRepository
from .handlers import DataPlane
from .rest import RESTServer
from .grpc import GRPCServer

HANDLED_SIGNALS = [signal.SIGINT, signal.SIGTERM]


class MLServer:
    def __init__(self, settings: Settings):
        self._model_repository = ModelRepository()
        self._settings = settings
        self._data_plane = DataPlane(
            settings=self._settings, model_repository=self._model_repository
        )

    async def start(self, models: List[MLModel] = []):
        self._add_signal_handlers()

        load_tasks = [self._model_repository.load(model) for model in models]
        await asyncio.gather(*load_tasks)

        self._rest_server = RESTServer(self._settings, self._data_plane)
        self._grpc_server = GRPCServer(self._settings, self._data_plane)
        await asyncio.gather(self._rest_server.start(), self._grpc_server.start())

    def _add_signal_handlers(self):
        loop = asyncio.get_event_loop()

        for sign in HANDLED_SIGNALS:
            loop.add_signal_handler(sign, lambda: asyncio.ensure_future(self.stop()))

    async def stop(self):
        await self._rest_server.stop()
        await self._grpc_server.stop()
