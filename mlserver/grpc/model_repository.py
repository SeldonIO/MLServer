from typing import Callable

from . import model_repository_pb2 as mr_pb
from .converters import (
    RepositoryIndexRequestConverter,
    RepositoryIndexResponseConverter,
)
from .model_repository_pb2_grpc import ModelRepositoryServiceServicer
from .utils import handle_mlserver_error
from .logging import logger
from ..handlers import ModelRepositoryHandlers


def _deprecated(f: Callable):
    async def _inner(self, request, context):
        logger.warning(
            "DEPRECATED!! "
            f"The `inference.model_repository.ModelRepositoryService/{f.__name__}` "
            "endpoint has now been deprecated and will be removed in "
            "MLServer 1.2.0. "
            f"Please use the `inference.GRPCInferenceService/{f.__name__}` "
            "endpoint instead."
        )
        return await f(self, request, context)

    return _inner


class ModelRepositoryServicer(ModelRepositoryServiceServicer):
    def __init__(self, handlers: ModelRepositoryHandlers):
        self._handlers = handlers

    @_deprecated
    async def RepositoryIndex(
        self, request: mr_pb.RepositoryIndexRequest, context
    ) -> mr_pb.RepositoryIndexResponse:
        payload = RepositoryIndexRequestConverter.to_types(request)
        index = await self._handlers.index(payload)
        return RepositoryIndexResponseConverter.from_types(  # type: ignore
            index, use_model_repository=True
        )

    @handle_mlserver_error
    @_deprecated
    async def RepositoryModelLoad(
        self, request: mr_pb.RepositoryModelLoadRequest, context
    ) -> mr_pb.RepositoryModelLoadResponse:
        await self._handlers.load(request.model_name)
        return mr_pb.RepositoryModelLoadResponse()

    @handle_mlserver_error
    @_deprecated
    async def RepositoryModelUnload(
        self, request: mr_pb.RepositoryModelUnloadRequest, context
    ) -> mr_pb.RepositoryModelUnloadResponse:
        await self._handlers.unload(request.model_name)
        return mr_pb.RepositoryModelUnloadResponse()
