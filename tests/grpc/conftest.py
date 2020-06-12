import os
import pytest
import grpc

from google.protobuf import json_format
from mlserver.handlers import DataPlane
from mlserver.settings import Settings
from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from mlserver.grpc import create_server

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
def grpc_settings() -> Settings:
    return Settings(debug=True, grpc_workers=1)


@pytest.fixture
def inference_service_stub(grpc_server, grpc_settings) -> GRPCInferenceServiceStub:
    channel = grpc.insecure_channel(f"[::]:{grpc_settings.grpc_port}")
    return GRPCInferenceServiceStub(channel)


@pytest.fixture
def grpc_server(grpc_settings, data_plane: DataPlane):
    server = create_server(grpc_settings, data_plane)
    server.start()

    yield server

    ev = server.stop(grace=None)
    ev.wait()
