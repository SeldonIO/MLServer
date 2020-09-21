import os
import pytest

from grpc.experimental import aio

from google.protobuf import json_format
from mlserver.handlers import DataPlane
from mlserver.settings import Settings
from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from mlserver.grpc import GRPCServer

from ..conftest import TESTDATA_PATH

TESTDATA_GRPC_PATH = os.path.join(TESTDATA_PATH, "grpc")


def _read_testdata_pb(payload_path: str, pb_klass):
    model_infer_request = pb_klass()
    with open(payload_path) as payload:
        json_format.Parse(payload.read(), model_infer_request)

    return model_infer_request


@pytest.fixture
def model_infer_request() -> pb.ModelInferRequest:
    payload_path = os.path.join(TESTDATA_GRPC_PATH, "model-infer-request.json")
    return _read_testdata_pb(payload_path, pb.ModelInferRequest)


@pytest.fixture
def grpc_settings(settings: Settings) -> Settings:
    settings.grpc_workers = 1
    return settings


@pytest.fixture
async def inference_service_stub(
    grpc_server, grpc_settings: Settings
) -> GRPCInferenceServiceStub:
    async with aio.insecure_channel(
        f"{grpc_settings.host}:{grpc_settings.grpc_port}"
    ) as channel:
        yield GRPCInferenceServiceStub(channel)


@pytest.fixture
async def grpc_server(grpc_settings: Settings, data_plane: DataPlane):
    server = GRPCServer(grpc_settings, data_plane)
    server._create_server()
    await server._server.start()

    yield server

    await server._server.stop(grace=None)
