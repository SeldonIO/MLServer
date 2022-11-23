import grpc

from typing import Callable, Dict, Tuple
from fastapi import status

from grpc import ServicerContext

from .logging import logger
from ..errors import MLServerError


STATUS_CODE_MAPPING = {
    status.HTTP_400_BAD_REQUEST: grpc.StatusCode.INVALID_ARGUMENT,
    status.HTTP_404_NOT_FOUND: grpc.StatusCode.NOT_FOUND,
    status.HTTP_422_UNPROCESSABLE_ENTITY: grpc.StatusCode.FAILED_PRECONDITION,
    status.HTTP_500_INTERNAL_SERVER_ERROR: grpc.StatusCode.INTERNAL,
}


def to_headers(context: ServicerContext) -> Dict[str, str]:
    metadata = context.invocation_metadata()
    if hasattr(context, "trailing_metadata"):
        # NOTE: Older versions of `grpcio` (e.g. `grpcio==1.34.0`) don't expose
        # access to the trailing metadata on the service side
        metadata += context.trailing_metadata()
    headers = {}
    for metadatum in metadata:
        headers[metadatum.key] = metadatum.value

    return headers


def to_metadata(headers: Dict[str, str]) -> Tuple[Tuple[str, str], ...]:
    return tuple((key.lower(), value) for key, value in headers.items())


def _grpc_status_code(err: MLServerError):
    return STATUS_CODE_MAPPING.get(err.status_code, grpc.StatusCode.UNKNOWN)


def handle_mlserver_error(f: Callable):
    async def _inner(self, request, context):
        try:
            return await f(self, request, context)
        except MLServerError as err:
            logger.exception(err)
            await context.abort(code=_grpc_status_code(err), details=str(err))
        except Exception as err:
            logger.exception(err)
            await context.abort(code=grpc.StatusCode.INTERNAL, details=str(err))

    return _inner
