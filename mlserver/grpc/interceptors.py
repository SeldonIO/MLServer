import logging

from typing import Callable, Awaitable

from grpc.aio import ServerInterceptor
from grpc import HandlerCallDetails, RpcMethodHandler


class LoggingInterceptor(ServerInterceptor):
    def __init__(self):
        self._mlserver_grpc = logging.getLogger("mlserver.grpc")

    def _get_log_message(self, handler_call_details: HandlerCallDetails) -> str:
        return handler_call_details.method

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        self._mlserver_grpc.info(self._get_log_message(handler_call_details))
        handler = await continuation(handler_call_details)
        return handler
