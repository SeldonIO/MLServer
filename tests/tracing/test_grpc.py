import json

from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub


# Import fixture from `grpc` module
from ..grpc.conftest import model_infer_request  # noqa: F401


async def test_grpc_metrics(
    span_exporter: InMemorySpanExporter,
    inference_service_stub: GRPCInferenceServiceStub,
    model_infer_request: pb.ModelInferRequest,  # noqa: F811
):
    _ = await inference_service_stub.ModelInfer(model_infer_request)

    spans = [json.loads(span.to_json()) for span in span_exporter.get_finished_spans()]
    assert len(spans) == 1

    span = spans[0]
    assert span["name"] == "/inference.GRPCInferenceService/ModelInfer"
    assert (
        "service.name.testing" in span["resource"]["attributes"]
        and span["resource"]["attributes"]["service.name.testing"] == "mlserver-testing"
    )
    assert span["kind"] == "SpanKind.SERVER"
    assert span["parent_id"] is None
