import grpc

from . import dataplane_pb2 as pb
from .dataplane_pb2_grpc import GRPCInferenceServiceServicer
from .converters import (
    ModelInferRequestConverter,
    ModelInferResponseConverter,
    ServerMetadataResponseConverter,
    ModelMetadataResponseConverter,
    RepositoryIndexRequestConverter,
    RepositoryIndexResponseConverter,
)
from .utils import to_headers, to_metadata, handle_mlserver_error

from ..utils import insert_headers, extract_headers
from ..handlers import DataPlane, ModelRepositoryHandlers


class InferenceServicer(GRPCInferenceServiceServicer):
    def __init__(
        self, data_plane: DataPlane, model_repository_handlers: ModelRepositoryHandlers
    ):
        super().__init__()
        self._data_plane = data_plane
        self._model_repository_handlers = model_repository_handlers

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

    @handle_mlserver_error
    async def ModelMetadata(
        self, request: pb.ModelMetadataRequest, context
    ) -> pb.ModelMetadataResponse:
        metadata = await self._data_plane.model_metadata(
            name=request.name, version=request.version
        )
        return ModelMetadataResponseConverter.from_types(metadata)

    @handle_mlserver_error
    async def ModelInfer(
        self, request: pb.ModelInferRequest, context: grpc.ServicerContext
    ) -> pb.ModelInferResponse:
        return_raw = False
        if request.raw_input_contents:
            # If the request contains raw input contents, then use the same for
            # the output
            return_raw = True

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

        response = ModelInferResponseConverter.from_types(result, use_raw=return_raw)
        return response

    async def RepositoryIndex(
        self, request: pb.RepositoryIndexRequest, context
    ) -> pb.RepositoryIndexResponse:
        payload = RepositoryIndexRequestConverter.to_types(request)
        index = await self._model_repository_handlers.index(payload)
        return RepositoryIndexResponseConverter.from_types(index)  # type: ignore

    @handle_mlserver_error
    async def RepositoryModelLoad(
        self, request: pb.RepositoryModelLoadRequest, context
    ) -> pb.RepositoryModelLoadResponse:
        await self._model_repository_handlers.load(request.model_name)
        return pb.RepositoryModelLoadResponse()

    @handle_mlserver_error
    async def RepositoryModelUnload(
        self, request: pb.RepositoryModelUnloadRequest, context
    ) -> pb.RepositoryModelUnloadResponse:
        await self._model_repository_handlers.unload(request.model_name)
        return pb.RepositoryModelUnloadResponse()
