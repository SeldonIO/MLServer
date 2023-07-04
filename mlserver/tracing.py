from typing import Optional

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter

from mlserver.settings import Settings


_TRACER_PROVIDER: Optional[TracerProvider] = None


def _create_resource(settings: Settings) -> Resource:
    return Resource(
        attributes={
            SERVICE_NAME: settings.server_name,
            SERVICE_VERSION: settings.server_version,
        }
    )


def _create_span_exporter(settings: Settings) -> SpanExporter:
    return OTLPSpanExporter(insecure=True, endpoint=settings.tracing_server)


def get_tracer_provider(settings: Settings) -> TracerProvider:
    global _TRACER_PROVIDER
    if _TRACER_PROVIDER is not None:
        return _TRACER_PROVIDER

    resource = _create_resource(settings)
    tracer_provider = TracerProvider(resource=resource)
    span_exporter = _create_span_exporter(settings)
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    _TRACER_PROVIDER = tracer_provider
    return _TRACER_PROVIDER
