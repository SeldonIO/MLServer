import asyncio

from typing import List

from .model import MLModel
from .settings import Settings
from .repository import ModelRepository
from .handlers import DataPlane
from .rest import RESTServer
from .grpc import GRPCServer


class MLServer:
    def __init__(self, settings: Settings):
        self._model_repository = ModelRepository()
        self._settings = settings
        self._data_plane = DataPlane(
            settings=self._settings, model_repository=self._model_repository
        )

    async def start(self, models: List[MLModel] = []):
        load_tasks = [self._model_repository.load(model) for model in models]
        await asyncio.gather(*load_tasks)

        self._rest_server = RESTServer(self._settings, self._data_plane)
        self._grpc_server = GRPCServer(self._settings, self._data_plane)
        await asyncio.gather(self._rest_server.start(), self._grpc_server.start())
