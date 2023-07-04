import json

from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mlserver.model import MLModel
from mlserver.types import InferenceRequest

from ..utils import RESTClient


async def test_tracing(
    span_exporter: InMemorySpanExporter,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()

    _ = await rest_client.infer(sum_model.name, inference_request)

    spans = [json.loads(span.to_json()) for span in span_exporter.get_finished_spans()]
    assert len(spans) > 0

    trace_ids = set()
    for s in spans:
        assert "/v2/models/{model_name}/infer" in s["name"]
        assert (
            "service.name.testing" in s["resource"]["attributes"]
            and s["resource"]["attributes"]["service.name.testing"]
            == "mlserver-testing"
        )
        trace_ids.add(s["context"]["trace_id"])
    assert len(trace_ids) == 1

    server_spans = [s for s in spans if s["kind"] == "SpanKind.SERVER"]
    assert len(server_spans) == 1
    assert server_spans[0]["parent_id"] is None
