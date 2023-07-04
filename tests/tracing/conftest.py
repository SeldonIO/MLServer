from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from mlserver import Settings, MLServer
from pytest import fixture
from typing import AsyncGenerator
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from grpc import aio


@fixture
def settings(settings: Settings) -> Settings:
    settings.tracing_server = "something:port"
    return settings


@fixture
def span_exporter(mocker) -> SpanExporter:
    span_exporter = InMemorySpanExporter()
    mocker.patch("mlserver.tracing._create_span_exporter", return_value=span_exporter)
    yield span_exporter
    span_exporter.clear()


@fixture(autouse=True)
def tracer_provider(mocker, span_exporter, settings) -> TracerProvider:
    resource = Resource(attributes={"service.name.testing": "mlserver-testing"})
    tracer_provider = TracerProvider(resource=resource)
    span_processor = SimpleSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    mocker.patch("mlserver.rest.app.get_tracer_provider", return_value=tracer_provider)
    mocker.patch(
        "mlserver.grpc.server.get_tracer_provider", return_value=tracer_provider
    )
    yield tracer_provider
    tracer_provider.shutdown()


@fixture
async def inference_service_stub(
    mlserver: MLServer, settings: Settings
) -> AsyncGenerator[GRPCInferenceServiceStub, None]:
    async with aio.insecure_channel(f"{settings.host}:{settings.grpc_port}") as channel:
        yield GRPCInferenceServiceStub(channel)
