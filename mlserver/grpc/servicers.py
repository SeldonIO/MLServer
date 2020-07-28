import grpc

from typing import Callable

from . import dataplane_pb2 as pb
from .dataplane_pb2_grpc import GRPCInferenceServiceServicer
from .converters import (
    ModelInferRequestConverter,
    ModelInferResponseConverter,
    ServerMetadataResponseConverter,
    ModelMetadataResponseConverter,
)

from ..handlers import DataPlane
from ..errors import MLServerError


def _handle_mlserver_error(f: Callable):
    def _inner(self, request, context):
        try:
            return f(self, request, context)
        except MLServerError as err:
            # TODO: Log error and stacktrace
            context.abort(code=grpc.StatusCode.INVALID_ARGUMENT, details=str(err))

    return _inner


class InferenceServicer(GRPCInferenceServiceServicer):
    def __init__(self, data_plane: DataPlane):
        super().__init__()
        self._data_plane = data_plane

    def ServerLive(
        self, request: pb.ServerLiveRequest, context
    ) -> pb.ServerLiveResponse:
        is_live = self._data_plane.live()
        return pb.ServerLiveResponse(live=is_live)

    def ServerReady(
        self, request: pb.ServerReadyRequest, context
    ) -> pb.ServerReadyResponse:
        is_ready = self._data_plane.ready()
        return pb.ServerReadyResponse(ready=is_ready)

    def ModelReady(
        self, request: pb.ModelReadyRequest, context
    ) -> pb.ModelReadyResponse:
        is_model_ready = self._data_plane.model_ready(
            name=request.name, version=request.version
        )
        return pb.ModelReadyResponse(ready=is_model_ready)

    def ServerMetadata(
        self, request: pb.ServerMetadataRequest, context
    ) -> pb.ServerMetadataResponse:
        metadata = self._data_plane.metadata()
        return ServerMetadataResponseConverter.from_types(metadata)

    @_handle_mlserver_error
    def ModelMetadata(
        self, request: pb.ModelMetadataRequest, context
    ) -> pb.ModelMetadataResponse:
        metadata = self._data_plane.model_metadata(
            name=request.name, version=request.version
        )
        return ModelMetadataResponseConverter.from_types(metadata)

    @_handle_mlserver_error
    def ModelInfer(
        self, request: pb.ModelInferRequest, context
    ) -> pb.ModelInferResponse:
        payload = ModelInferRequestConverter.to_types(request)
        result = self._data_plane.infer(
            payload=payload, name=request.model_name, version=request.model_version
        )
        response = ModelInferResponseConverter.from_types(result)
        return response
