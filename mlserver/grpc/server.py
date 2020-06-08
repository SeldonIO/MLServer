import grpc
from concurrent.futures import ThreadPoolExecutor

from ..handlers import DataPlane
from ..settings import Settings

from .servicers import InferenceServicer
from .dataplane_pb2_grpc import add_GRPCInferenceServiceServicer_to_server


def create_server(settings: Settings, data_plane: DataPlane) -> grpc.Server:
    servicer = InferenceServicer(data_plane)

    server = grpc.server(ThreadPoolExecutor(max_workers=settings.grpc_workers))

    add_GRPCInferenceServiceServicer_to_server(servicer, server)

    server.add_insecure_port(f"[::]:{settings.grpc_port}")

    return server
