import os
import pytest

from grpc import aio

from typing import AsyncGenerator, Dict
from google.protobuf import json_format

from mlserver.parallel import load_inference_pool, unload_inference_pool
from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.settings import Settings
from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc import model_repository_pb2 as mr_pb
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from mlserver.grpc.model_repository_pb2_grpc import ModelRepositoryServiceStub
from mlserver.grpc import GRPCServer

from ..conftest import TESTDATA_PATH
from ..fixtures import SumModel

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
def grpc_repository_index_request() -> mr_pb.RepositoryIndexRequest:
    return mr_pb.RepositoryIndexRequest(ready=None)


@pytest.fixture
def grpc_parameters() -> Dict[str, pb.InferParameter]:
    return {
        "content_type": pb.InferParameter(string_param="np"),
        "foo": pb.InferParameter(bool_param=True),
        "bar": pb.InferParameter(int64_param=46),
    }


@pytest.fixture
async def inference_service_stub(
    grpc_server, grpc_settings: Settings
) -> AsyncGenerator[GRPCInferenceServiceStub, None]:
    async with aio.insecure_channel(
        f"{grpc_settings.host}:{grpc_settings.grpc_port}"
    ) as channel:
        yield GRPCInferenceServiceStub(channel)


@pytest.fixture
async def model_repository_service_stub(
    grpc_server, grpc_settings: Settings
) -> AsyncGenerator[ModelRepositoryServiceStub, None]:
    async with aio.insecure_channel(
        f"{grpc_settings.host}:{grpc_settings.grpc_port}"
    ) as channel:
        yield ModelRepositoryServiceStub(channel)


@pytest.fixture
async def grpc_server(
    grpc_settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    sum_model: SumModel,
):
    server = GRPCServer(
        grpc_settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    server._create_server()

    await load_inference_pool(sum_model)
    await server._server.start()

    yield server

    await unload_inference_pool(sum_model)
    await server._server.stop(grace=None)
