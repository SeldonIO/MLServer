from grpc import aio
from concurrent.futures import ThreadPoolExecutor

from ..handlers import DataPlane, ModelRepositoryHandlers
from ..settings import Settings

from .servicers import InferenceServicer, ModelRepositoryServicer
from .dataplane_pb2_grpc import add_GRPCInferenceServiceServicer_to_server
from .model_repository_pb2_grpc import add_ModelRepositoryServiceServicer_to_server


class GRPCServer:
    def __init__(
        self,
        settings: Settings,
        data_plane: DataPlane,
        model_repository_handlers: ModelRepositoryHandlers,
    ):
        self._settings = settings
        self._data_plane = data_plane
        self._model_repository_handlers = model_repository_handlers

    def _create_server(self):
        self._inference_servicer = InferenceServicer(self._data_plane)
        self._model_repository_servicer = ModelRepositoryServicer(
            self._model_repository_handlers
        )
        self._server = aio.server(
            ThreadPoolExecutor(max_workers=self._settings.grpc_workers)
        )

        add_GRPCInferenceServiceServicer_to_server(
            self._inference_servicer, self._server
        )
        add_ModelRepositoryServiceServicer_to_server(
            self._model_repository_servicer, self._server
        )

        self._server.add_insecure_port(
            f"{self._settings.host}:{self._settings.grpc_port}"
        )

        return self._server

    async def start(self):
        self._create_server()

        await self._server.start()
        await self._server.wait_for_termination()

    async def stop(self):
        # TODO: Read from config
        await self._server.stop(grace=5)
