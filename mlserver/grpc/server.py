from grpc.experimental import aio
from concurrent.futures import ThreadPoolExecutor

from ..handlers import DataPlane
from ..settings import Settings

from .servicers import InferenceServicer
from .dataplane_pb2_grpc import add_GRPCInferenceServiceServicer_to_server


class GRPCServer:
    def __init__(self, settings: Settings, data_plane: DataPlane):
        self._settings = settings
        self._data_plane = data_plane

    def _create_server(self):
        self._servicer = InferenceServicer(self._data_plane)
        self._server = aio.server(
            ThreadPoolExecutor(max_workers=self._settings.grpc_workers)
        )

        add_GRPCInferenceServiceServicer_to_server(self._servicer, self._server)

        self._server.add_insecure_port(f"[::]:{self._settings.grpc_port}")

        return self._server

    async def start(self):
        self._create_server()

        await self._server.start()
        await self._server.wait_for_termination()

    async def stop(self):
        # TODO: Read from config
        await self._server.stop(grace=5)
