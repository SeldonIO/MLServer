from prometheus_client import Counter
from prometheus_client import Histogram

def init_metrics(registry):
  return {
      "grpc_server_started_counter": Counter(
          "grpc_server_started_total",
          "Total number of RPCs started on the server.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),
      "grpc_server_stream_msg_received": Counter(
          "grpc_server_msg_received_total",
          "Total number of RPC stream messages received on the server.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),
      "grpc_server_stream_msg_sent": Counter(
          "grpc_server_msg_sent_total",
          "Total number of gRPC stream messages sent by the server.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),
      "grpc_server_handled_histogram": Histogram(
          "grpc_server_handling_seconds",
          "Histogram of response latency (seconds) of gRPC that had been application-level "
          "handled by the server.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),
      "legacy_grpc_server_handled_latency_seconds": Histogram(
          "grpc_server_handled_latency_seconds",
          "Histogram of response latency (seconds) of gRPC that had been "
          "application-level handled by the server",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      )
  }


# Legacy metrics for backward compatibility
def get_grpc_server_handled_counter(is_legacy, registry):
  if is_legacy:
    return Counter(
        "grpc_server_handled_total",
        "Total number of RPCs completed on the server, regardless of success or failure.",
        ["grpc_type", "grpc_service", "grpc_method", "code"],
        registry=registry
    )
  return Counter(
      "grpc_server_handled_total",
      "Total number of RPCs completed on the server, regardless of success or failure.",
      ["grpc_type", "grpc_service", "grpc_method", "grpc_code"],
      registry=registry
  )
