# Module `mlserver.grpc.interceptors`


## Class `LoggingInterceptor`


**Description:**
Affords intercepting incoming RPCs on the service-side.
This is an EXPERIMENTAL API.

### Method `intercept_service`


**Signature:** `intercept_service(self, continuation: Callable[[grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]], handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler`


**Description:**
Intercepts incoming RPCs before handing them over to a handler.
State can be passed from an interceptor to downstream interceptors
via contextvars. The first interceptor is called from an empty
contextvars.Context, and the same Context is used for downstream
interceptors and for the final handler call. Note that there are no
guarantees that interceptors and handlers will be called from the
same thread.

**Parameters:**
- `continuation` (unknown): A function that takes a HandlerCallDetails and
proceeds to invoke the next interceptor in the chain, if any,
or the RPC handler lookup logic, with the call details passed
as an argument, and returns an RpcMethodHandler instance if
the RPC is considered serviced, or None otherwise.
- `handler_call_details` (unknown): A HandlerCallDetails describing the RPC.

**Returns:**
- (unknown): An RpcMethodHandler with which the RPC may be serviced if the
interceptor chooses to service this RPC, or None otherwise.

## Class `PromServerInterceptor`


**Description:**
Simple wrapper around `py_grpc_prometheus` to support `grpc.aio`.
TODO: Open PR to add support upstream for AsyncIO.

### Method `intercept_service`


**Signature:** `intercept_service(self, continuation: Callable[[grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]], handler_call_details: grpc.HandlerCallDetails) -> grpc.RpcMethodHandler`


**Description:**
Intercepts incoming RPCs before handing them over to a handler.
State can be passed from an interceptor to downstream interceptors
via contextvars. The first interceptor is called from an empty
contextvars.Context, and the same Context is used for downstream
interceptors and for the final handler call. Note that there are no
guarantees that interceptors and handlers will be called from the
same thread.

**Parameters:**
- `continuation` (unknown): A function that takes a HandlerCallDetails and
proceeds to invoke the next interceptor in the chain, if any,
or the RPC handler lookup logic, with the call details passed
as an argument, and returns an RpcMethodHandler instance if
the RPC is considered serviced, or None otherwise.
- `handler_call_details` (unknown): A HandlerCallDetails describing the RPC.

**Returns:**
- (unknown): An RpcMethodHandler with which the RPC may be serviced if the
interceptor chooses to service this RPC, or None otherwise.

## Function `wrap_async_iterator_inc_counter`


**Signature:** `wrap_async_iterator_inc_counter(iterator: AsyncIterator[dataplane_pb2.ModelInferRequest], counter: prometheus_client.metrics.Counter, grpc_type: str, grpc_service_name: str, grpc_method_name: str) -> AsyncIterator[dataplane_pb2.ModelInferRequest]`


**Description:**
Wraps an async iterator and collect metrics.
