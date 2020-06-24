from . import dataplane_pb2 as pb
from .dataplane_pb2_grpc import GRPCInferenceServiceServicer
from .converters import (
    ModelInferRequestConverter,
    ModelInferResponseConverter,
    ServerMetadataResponseConverter,
    ModelMetadataResponseConverter,
)

from ..handlers import DataPlane


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
        is_model_ready = self._data_plane.model_ready(model_name=request.name)
        return pb.ModelReadyResponse(ready=is_model_ready)

    def ServerMetadata(
        self, request: pb.ServerMetadataRequest, context
    ) -> pb.ServerMetadataResponse:
        metadata = self._data_plane.metadata()
        return ServerMetadataResponseConverter.from_types(metadata)

    def ModelMetadata(
        self, request: pb.ModelMetadataRequest, context
    ) -> pb.ModelMetadataResponse:
        metadata = self._data_plane.model_metadata(model_name=request.name)
        return ModelMetadataResponseConverter.from_types(metadata)

    def ModelInfer(
        self, request: pb.ModelInferRequest, context
    ) -> pb.ModelInferResponse:
        payload = ModelInferRequestConverter.to_types(request)
        result = self._data_plane.infer(model_name=request.model_name, payload=payload)
        response = ModelInferResponseConverter.from_types(result)
        return response
