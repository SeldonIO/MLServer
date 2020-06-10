from . import dataplane_pb2 as pb
from .dataplane_pb2_grpc import GRPCInferenceServiceServicer
from .converters import ModelInferRequestConverter, ModelInferResponseConverter

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

    def ServerReady(self, request, context):
        pass

    def ModelReady(self, request, context):
        pass

    def ServerMetadata(self, request, context):
        pass

    def ModelMetadata(self, request, context):
        pass

    def ModelInfer(
        self, request: pb.ModelInferRequest, context
    ) -> pb.ModelInferResponse:
        payload = ModelInferRequestConverter.to_types(request)
        result = self.data_plane.infer(model_name=request.model_name, payload=payload)
        response = ModelInferResponseConverter.to_types(result)
        return response
