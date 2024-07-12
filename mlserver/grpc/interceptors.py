from typing import Awaitable, Callable, Tuple
from functools import partial
from timeit import default_timer

from grpc.aio import ServerInterceptor, ServicerContext
from grpc import HandlerCallDetails, RpcMethodHandler, RpcError, StatusCode
from py_grpc_prometheus.prometheus_server_interceptor import (
    grpc_utils,
    PromServerInterceptor as _PromServerInterceptor,
)

from .logging import logger


class LoggingInterceptor(ServerInterceptor):
    def _get_log_message(self, handler_call_details: HandlerCallDetails) -> str:
        return handler_call_details.method

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        logger.info(self._get_log_message(handler_call_details))
        handler = await continuation(handler_call_details)
        return handler


class PromServerInterceptor(ServerInterceptor):
    """
    Simple wrapper around `py_grpc_prometheus` to support `grpc.aio`.

    TODO: Open PR to add support upstream for AsyncIO.
    """

    def __init__(self, *args, **kwargs):
        self._interceptor = _PromServerInterceptor(*args, **kwargs)
        # We need a status code mapping to ensure we can convert from an int:
        # https://groups.google.com/g/grpc-io/c/EdIXjMEaOyw/m/d3DeqmrJAAAJ
        self._status_codes = {code.value[0]: code for code in StatusCode}

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        method_call = grpc_utils.split_method_call(handler_call_details)
        handler = await continuation(handler_call_details)

        metrics_wrapper = partial(self._metrics_wrapper, method_call)
        return self._interceptor._wrap_rpc_behavior(handler, metrics_wrapper)

    def _metrics_wrapper(
        self,
        method_call: Tuple[str, str, str],
        behavior: RpcMethodHandler,
        request_streaming: bool,
        response_streaming: bool,
    ):
        """
        Port of `py-grpc-prometheus` metrics_wrapper method to work with gRPC's
        AsyncIO support.
        To see the original implementation, please check:

        https://github.com/lchenn/py-grpc-prometheus/blob/eb9dee1f0a4e57cef220193ee48021dc9a9f3d82/py_grpc_prometheus/prometheus_server_interceptor.py#L46-L120
        """
        grpc_service_name, grpc_method_name, _ = method_call

        async def new_behavior(request, servicer_context):
            response = None
            try:
                start = default_timer()
                grpc_type = grpc_utils.get_method_type(
                    request_streaming, response_streaming
                )

                try:
                    self._interceptor._metrics["grpc_server_started_counter"].labels(
                        grpc_type=grpc_type,
                        grpc_service=grpc_service_name,
                        grpc_method=grpc_method_name,
                    ).inc()

                    # Invoke the original rpc behavior.
                    # NOTE: This is the main change required with respect to
                    # the original implementation in `py-grpc-prometheus`.
                    response = await behavior(request, servicer_context)
                    self._interceptor.increase_grpc_server_handled_total_counter(
                        grpc_type,
                        grpc_service_name,
                        grpc_method_name,
                        self._compute_status_code(servicer_context).name,
                    )
                    return response

                except RpcError as e:
                    self._interceptor.increase_grpc_server_handled_total_counter(
                        grpc_type,
                        grpc_service_name,
                        grpc_method_name,
                        self._interceptor._compute_error_code(e).name,
                    )
                    raise e

                finally:
                    if self._interceptor._legacy:
                        self._interceptor._metrics[
                            "legacy_grpc_server_handled_latency_seconds"
                        ].labels(
                            grpc_type=grpc_type,
                            grpc_service=grpc_service_name,
                            grpc_method=grpc_method_name,
                        ).observe(
                            max(default_timer() - start, 0)
                        )
                    elif self._interceptor._enable_handling_time_histogram:
                        self._interceptor._metrics[
                            "grpc_server_handled_histogram"
                        ].labels(
                            grpc_type=grpc_type,
                            grpc_service=grpc_service_name,
                            grpc_method=grpc_method_name,
                        ).observe(
                            max(default_timer() - start, 0)
                        )
            except Exception as e:  # pylint: disable=broad-except
                # Allow user to skip the exceptions in order to maintain
                # the basic functionality in the server
                # The logging function in exception can be toggled with log_exceptions
                # in order to suppress the noise in logging
                if self._interceptor._skip_exceptions:
                    if self._interceptor._log_exceptions:
                        logger.error(e)

                    if response is None:
                        return response

                    return await behavior(request, servicer_context)
                raise e

        async def new_behavior_stream(
            request_async_iterator, servicer_context: ServicerContext
        ):
            response_async_iterator = None
            try:
                grpc_type = grpc_utils.get_method_type(
                    request_streaming, response_streaming
                )
                try:
                    request_async_iterator = wrap_async_iterator_inc_counter(
                        request_async_iterator,
                        self._interceptor._metrics["grpc_server_stream_msg_received"],
                        grpc_type,
                        grpc_service_name,
                        grpc_method_name,
                    )

                    # wrap the original behavior with the metrics
                    sent_metric = self._interceptor._metrics[
                        "grpc_server_stream_msg_sent"
                    ]
                    response_async_iterator = wrap_async_iterator_inc_counter(
                        behavior(request_async_iterator, servicer_context),
                        sent_metric,
                        grpc_type,
                        grpc_service_name,
                        grpc_method_name,
                    )

                    # invoke the original rpc behavior
                    async for item in response_async_iterator:
                        yield item

                except RpcError as e:
                    self._interceptor.increase_grpc_server_handled_total_counter(
                        grpc_type,
                        grpc_service_name,
                        grpc_method_name,
                        self._interceptor._compute_error_code(e).name,
                    )
                    raise e

            except Exception as e:  # pylint: disable=broad-except
                # Allow user to skip the exceptions in order to maintain
                # the basic functionality in the server
                # The logging function in exception can be toggled with log_exceptions
                # in order to suppress the noise in logging
                if self._interceptor._skip_exceptions:
                    if self._interceptor._log_exceptions:
                        logger.error(e)

                    if response_async_iterator is not None:
                        async for item in behavior(
                            request_async_iterator, servicer_context
                        ):
                            yield item
                raise e

        if request_streaming and response_streaming:
            return new_behavior_stream

        return new_behavior

    def _compute_status_code(self, servicer_context: ServicerContext) -> StatusCode:
        """
        This method is mostly copied from `py-grpc-prometheus`, with a couple
        minor changes to avoid using private APIs from ServicerContext which
        don't exist anymore in `grpc.aio`.
        To see the original implementation, please check:

        https://github.com/lchenn/py-grpc-prometheus/blob/eb9dee1f0a4e57cef220193ee48021dc9a9f3d82/py_grpc_prometheus/prometheus_server_interceptor.py#L127-L134
        """
        # Backwards compatibility for non-aio.
        # TODO: It's not clear yet how to check whether the context has been
        # cancelled with aio.
        if hasattr(servicer_context, "_state"):
            if servicer_context._state.client == "cancelled":
                return StatusCode.CANCELLED

        if not hasattr(servicer_context, "code"):
            return StatusCode.OK

        code = servicer_context.code()
        if code is None:
            return StatusCode.OK

        # NOTE: With gRPC AIO, the `code` can be a plain integer that needs to
        # be converted to an actual `StatusCode` entry
        if isinstance(code, int):
            if code not in self._status_codes:
                return StatusCode.UNKNOWN

            return self._status_codes[code]

        return code


async def wrap_async_iterator_inc_counter(
    iterator, counter, grpc_type, grpc_service_name, grpc_method_name
):
    """Wraps an async iterator and collect metrics."""

    async for item in iterator:
        counter.labels(
            grpc_type=grpc_type,
            grpc_service=grpc_service_name,
            grpc_method=grpc_method_name,
        ).inc()
        yield item
