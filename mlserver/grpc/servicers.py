import grpc

from typing import Callable
from fastapi import status

from . import dataplane_pb2 as pb
from . import model_repository_pb2 as mr_pb
from .dataplane_pb2_grpc import GRPCInferenceServiceServicer
from .model_repository_pb2_grpc import ModelRepositoryServiceServicer
from .converters import (
    ModelInferRequestConverter,
    ModelInferResponseConverter,
    ServerMetadataResponseConverter,
    ModelMetadataResponseConverter,
    RepositoryIndexRequestConverter,
    RepositoryIndexResponseConverter,
)
from .logging import logger
from .utils import to_headers, to_metadata

from ..utils import insert_headers, extract_headers
from ..handlers import DataPlane, ModelRepositoryHandlers
from ..errors import MLServerError

STATUS_CODE_MAPPING = {
    status.HTTP_400_BAD_REQUEST: grpc.StatusCode.INVALID_ARGUMENT,
    status.HTTP_404_NOT_FOUND: grpc.StatusCode.NOT_FOUND,
    status.HTTP_422_UNPROCESSABLE_ENTITY: grpc.StatusCode.FAILED_PRECONDITION,
    status.HTTP_500_INTERNAL_SERVER_ERROR: grpc.StatusCode.INTERNAL,
}


def _grpc_status_code(err: MLServerError):
    return STATUS_CODE_MAPPING.get(err.status_code, grpc.StatusCode.UNKNOWN)


def _handle_mlserver_error(f: Callable):
    async def _inner(self, request, context):
        try:
            return await f(self, request, context)
        except MLServerError as err:
            logger.error(err)
            await context.abort(code=_grpc_status_code(err), details=str(err))

    return _inner


class InferenceServicer(GRPCInferenceServiceServicer):
    def __init__(self, data_plane: DataPlane):
        super().__init__()
        self._data_plane = data_plane

    async def ServerLive(
        self, request: pb.ServerLiveRequest, context
    ) -> pb.ServerLiveResponse:
        is_live = await self._data_plane.live()
        return pb.ServerLiveResponse(live=is_live)

    async def ServerReady(
        self, request: pb.ServerReadyRequest, context
    ) -> pb.ServerReadyResponse:
        is_ready = await self._data_plane.ready()
        return pb.ServerReadyResponse(ready=is_ready)

    async def ModelReady(
        self, request: pb.ModelReadyRequest, context
    ) -> pb.ModelReadyResponse:
        is_model_ready = await self._data_plane.model_ready(
            name=request.name, version=request.version
        )
        return pb.ModelReadyResponse(ready=is_model_ready)

    async def ServerMetadata(
        self, request: pb.ServerMetadataRequest, context
    ) -> pb.ServerMetadataResponse:
        metadata = await self._data_plane.metadata()
        return ServerMetadataResponseConverter.from_types(metadata)

    @_handle_mlserver_error
    async def ModelMetadata(
        self, request: pb.ModelMetadataRequest, context
    ) -> pb.ModelMetadataResponse:
        metadata = await self._data_plane.model_metadata(
            name=request.name, version=request.version
        )
        return ModelMetadataResponseConverter.from_types(metadata)

    @_handle_mlserver_error
    async def ModelInfer(
        self, request: pb.ModelInferRequest, context: grpc.ServicerContext
    ) -> pb.ModelInferResponse:
        payload = ModelInferRequestConverter.to_types(request)

        request_headers = to_headers(context)
        insert_headers(payload, request_headers)

        result = await self._data_plane.infer(
            payload=payload, name=request.model_name, version=request.model_version
        )

        response_headers = extract_headers(result)
        if response_headers:
            response_metadata = to_metadata(response_headers)
            context.set_trailing_metadata(response_metadata)

        response = ModelInferResponseConverter.from_types(result)
        return response


class ModelRepositoryServicer(ModelRepositoryServiceServicer):
    def __init__(self, handlers: ModelRepositoryHandlers):
        self._handlers = handlers

    async def RepositoryIndex(
        self, request: mr_pb.RepositoryIndexRequest, context
    ) -> mr_pb.RepositoryIndexResponse:
        payload = RepositoryIndexRequestConverter.to_types(request)
        index = await self._handlers.index(payload)
        return RepositoryIndexResponseConverter.from_types(index)

    @_handle_mlserver_error
    async def RepositoryModelLoad(
        self, request: mr_pb.RepositoryModelLoadRequest, context
    ) -> mr_pb.RepositoryModelLoadResponse:
        await self._handlers.load(request.model_name)
        return mr_pb.RepositoryModelLoadResponse()

    @_handle_mlserver_error
    async def RepositoryModelUnload(
        self, request: mr_pb.RepositoryModelUnloadRequest, context
    ) -> mr_pb.RepositoryModelUnloadResponse:
        await self._handlers.unload(request.model_name)
        return mr_pb.RepositoryModelUnloadResponse()
