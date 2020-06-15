import uvicorn
import multiprocessing
from typing import List, Union

from .model import MLModel
from .settings import Settings
from .registry import ModelRegistry
from .handlers import DataPlane
from .rest import create_app
from .grpc import create_server


class MLServer:
    def __init__(self, settings: Settings, models: Union[List[MLModel], MLModel] = []):
        self._model_registry = ModelRegistry()
        self._settings = settings
        self._data_plane = DataPlane(self._model_registry)

        if not isinstance(models, list):
            models = [models]

        for model in models:
            self._model_registry.load(model.name, model)

    def start(self):
        self._rest_process = self._start(self._rest)
        self._grpc_process = self._start(self._grpc)

        self._rest_process.join()
        self._grpc_process.join()

    def _start(self, target: str):
        p = multiprocessing.Process(target=target)
        p.start()
        return p

    def _rest(self):
        app = create_app(self._settings, self._data_plane)
        uvicorn.run(app, port=self._settings.http_port)

    def _grpc(self):
        server = create_server(self._settings, self._data_plane)
        server.start()
        server.wait_for_termination()
