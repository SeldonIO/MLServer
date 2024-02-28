"""
NOTE: These tests belong to the deprecated ModelRepository API, which has now
been merged with the GRPCInferenceService's dataplane.
"""

import pytest
import grpc

from typing import AsyncGenerator
from grpc import aio

from mlserver.settings import Settings
from mlserver.grpc.converters import (
    RepositoryIndexRequestConverter,
    RepositoryIndexResponseConverter,
)
from mlserver.grpc.model_repository_pb2_grpc import ModelRepositoryServiceStub
from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc import model_repository_pb2 as mr_pb


@pytest.fixture
def grpc_repository_index_request() -> mr_pb.RepositoryIndexRequest:
    return mr_pb.RepositoryIndexRequest(ready=None)


@pytest.fixture
async def model_repository_service_stub(
    grpc_server, settings: Settings
) -> AsyncGenerator[ModelRepositoryServiceStub, None]:
    async with aio.insecure_channel(f"{settings.host}:{settings.grpc_port}") as channel:
        yield ModelRepositoryServiceStub(channel)


def test_repositoryindexrequest_to_types(grpc_repository_index_request):
    repository_index_request = RepositoryIndexRequestConverter.to_types(
        grpc_repository_index_request
    )

    assert repository_index_request.ready == grpc_repository_index_request.ready


def test_repositoryindexresponse_from_types(repository_index_response):
    grpc_repository_index_response = RepositoryIndexResponseConverter.from_types(
        repository_index_response, use_model_repository=True
    )

    assert isinstance(grpc_repository_index_response, mr_pb.RepositoryIndexResponse)
    assert len(grpc_repository_index_response.models) == len(repository_index_response)

    for expected, grpc_model in zip(
        repository_index_response, grpc_repository_index_response.models
    ):
        assert isinstance(grpc_model, mr_pb.RepositoryIndexResponse.ModelIndex)
        assert expected.name == grpc_model.name
        assert expected.version == grpc_model.version
        assert expected.state == grpc_model.state
        assert expected.reason == grpc_model.reason


async def test_model_repository_index(
    model_repository_service_stub, grpc_repository_index_request
):
    index = await model_repository_service_stub.RepositoryIndex(
        grpc_repository_index_request
    )

    assert len(index.models) == 1


async def test_model_repository_unload(
    inference_service_stub, model_repository_service_stub, sum_model_settings
):
    unload_request = mr_pb.RepositoryModelUnloadRequest(
        model_name=sum_model_settings.name
    )
    await model_repository_service_stub.RepositoryModelUnload(unload_request)

    with pytest.raises(grpc.RpcError):
        await inference_service_stub.ModelMetadata(
            pb.ModelMetadataRequest(name=sum_model_settings.name)
        )


async def test_model_repository_load(
    inference_service_stub,
    model_repository_service_stub,
    sum_model_settings,
):
    await model_repository_service_stub.RepositoryModelUnload(
        mr_pb.RepositoryModelLoadRequest(model_name=sum_model_settings.name)
    )

    load_request = mr_pb.RepositoryModelLoadRequest(model_name=sum_model_settings.name)
    await model_repository_service_stub.RepositoryModelLoad(load_request)

    response = await inference_service_stub.ModelMetadata(
        pb.ModelMetadataRequest(name=sum_model_settings.name)
    )

    assert response.name == sum_model_settings.name


async def test_model_repository_load_error(
    inference_service_stub,
    model_repository_service_stub,
    sum_model_settings,
):
    with pytest.raises(grpc.RpcError) as err:
        load_request = mr_pb.RepositoryModelLoadRequest(model_name="my-model")
        await model_repository_service_stub.RepositoryModelLoad(load_request)

    assert err.value.code() == grpc.StatusCode.NOT_FOUND
    assert err.value.details() == "Model my-model not found"
