UNARY = "UNARY"
SERVER_STREAMING = "SERVER_STREAMING"
CLIENT_STREAMING = "CLIENT_STREAMING"
BIDI_STREAMING = "BIDI_STREAMING"
UNKNOWN = "UNKNOWN"


def wrap_iterator_inc_counter(iterator, counter, grpc_type, grpc_service_name, grpc_method_name):
  """Wraps an iterator and collect metrics."""

  for item in iterator:
    counter.labels(
      grpc_type=grpc_type,
      grpc_service=grpc_service_name,
      grpc_method=grpc_method_name).inc()
    yield item


def get_method_type(request_streaming, response_streaming):
  """
  Infers the method type from if the request or the response is streaming.

  # The Method type is coming from:
  # https://grpc.io/grpc-java/javadoc/io/grpc/MethodDescriptor.MethodType.html
  """
  if request_streaming and response_streaming:
    return BIDI_STREAMING
  elif request_streaming and not response_streaming:
    return CLIENT_STREAMING
  elif not request_streaming and response_streaming:
    return SERVER_STREAMING
  return UNARY


def split_method_call(handler_call_details):
  """
  Infers the grpc service and method name from the handler_call_details.
  """

  # e.g. /package.ServiceName/MethodName
  parts = handler_call_details.method.split("/")
  if len(parts) < 3:
    return "", "", False

  grpc_service_name, grpc_method_name = parts[1:3]
  return grpc_service_name, grpc_method_name, True
