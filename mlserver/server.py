import multiprocessing
from typing import List, Callable

from .model import MLModel
from .settings import Settings
from .repository import ModelRepository
from .handlers import DataPlane
from .rest import RESTServer
from .grpc import GRPCServer


class MLServer:
    def __init__(self, settings: Settings, models: List[MLModel] = []):
        self._model_repository = ModelRepository()
        self._settings = settings
        self._data_plane = DataPlane(
            settings=self._settings, model_repository=self._model_repository
        )

        # TODO: Figure out how to load async on startup
        #  for model in models:
        #  self._model_repository.load(model)

    def start(self):
        # TODO: Explore using gRPC's AsyncIO support to run on single event
        # loop
        self._rest_server = RESTServer(self._settings, self._data_plane)
        self._grpc_server = GRPCServer(self._settings, self._data_plane)

        self._rest_process = self._start(self._rest_server.start)
        self._grpc_process = self._start(self._grpc_server.start)

        self._rest_process.join()
        self._grpc_process.join()

    def _start(self, target: Callable):
        p = multiprocessing.Process(target=target)
        p.start()
        return p
