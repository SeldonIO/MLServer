from . import model_repository_pb2 as mr_pb
from .converters import (
    RepositoryIndexRequestConverter,
    RepositoryIndexResponseConverter,
)
from .model_repository_pb2_grpc import ModelRepositoryServiceServicer
from .utils import handle_mlserver_error
from ..handlers import ModelRepositoryHandlers


class ModelRepositoryServicer(ModelRepositoryServiceServicer):
    def __init__(self, handlers: ModelRepositoryHandlers):
        self._handlers = handlers

    # TODO: Add deprecation note
    async def RepositoryIndex(
        self, request: mr_pb.RepositoryIndexRequest, context
    ) -> mr_pb.RepositoryIndexResponse:
        payload = RepositoryIndexRequestConverter.to_types(request)
        index = await self._handlers.index(payload)
        return RepositoryIndexResponseConverter.from_types(  # type: ignore
            index, use_model_repository=True
        )

    @handle_mlserver_error
    async def RepositoryModelLoad(
        self, request: mr_pb.RepositoryModelLoadRequest, context
    ) -> mr_pb.RepositoryModelLoadResponse:
        await self._handlers.load(request.model_name)
        return mr_pb.RepositoryModelLoadResponse()

    @handle_mlserver_error
    async def RepositoryModelUnload(
        self, request: mr_pb.RepositoryModelUnloadRequest, context
    ) -> mr_pb.RepositoryModelUnloadResponse:
        await self._handlers.unload(request.model_name)
        return mr_pb.RepositoryModelUnloadResponse()
