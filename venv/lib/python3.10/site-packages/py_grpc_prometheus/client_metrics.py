from prometheus_client import Counter
from prometheus_client import Histogram

def init_metrics(registry):
  return {
      "grpc_client_started_counter": Counter(
          "grpc_client_started_total",
          "Total number of RPCs started on the client",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),

      "grpc_client_handled_counter": Counter(
          "grpc_client_handled_total",
          "Total number of RPCs completed on the client, "
          "regardless of success or failure.",
          ["grpc_type", "grpc_service", "grpc_method", "grpc_code"],
          registry=registry
      ),

      "grpc_client_stream_msg_received": Counter(
          "grpc_client_msg_received_total",
          "Total number of RPC stream messages received by the client.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),

      "grpc_client_stream_msg_sent": Counter(
          "grpc_client_msg_sent_total",
          "Total number of gRPC stream messages sent by the client.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),

      "grpc_client_handled_histogram": Histogram(
          "grpc_client_handling_seconds",
          "Histogram of response latency (seconds) of the gRPC until" \
            "it is finished by the application.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),

      "grpc_client_stream_recv_histogram": Histogram(
          "grpc_client_msg_recv_handling_seconds",
          "Histogram of response latency (seconds) of the gRPC single message receive.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),

      "grpc_client_stream_send_histogram": Histogram(
          "grpc_client_msg_send_handling_seconds",
          "Histogram of response latency (seconds) of the gRPC single message send.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),

      # Legacy metrics for backwards compatibility

      "legacy_grpc_client_completed_counter": Counter(
          "grpc_client_completed",
          "Total number of RPCs completed on the client, "
          "regardless of success or failure.",
          ["grpc_type", "grpc_service", "grpc_method", "code"],
          registry=registry
      ),

      "legacy_grpc_client_completed_latency_seconds_histogram": Histogram(
          "grpc_client_completed_latency_seconds",
          "Histogram of rpc response latency (in seconds) for completed rpcs.",
          ["grpc_type", "grpc_service", "grpc_method"],
          registry=registry
      ),
  }
