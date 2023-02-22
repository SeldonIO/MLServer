import pytest

from mlserver.server import MLServer
from mlserver.settings import Settings
from mlserver.metrics.prometheus import PrometheusEndpoint
from mlserver.metrics.registry import REGISTRY, MetricsRegistry

from .utils import MetricsClient


@pytest.fixture
def metrics_registry() -> MetricsRegistry:
    yield REGISTRY

    # NOTE: Since the `REGISTRY` object is global, this fixture is NOT
    # thread-safe!!
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)


@pytest.fixture
def prometheus_endpoint(settings: Settings) -> PrometheusEndpoint:
    return PrometheusEndpoint(settings)


@pytest.fixture
async def metrics_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.metrics_port}"
    client = MetricsClient(http_server, metrics_endpoint=settings.metrics_endpoint)

    yield client

    await client.close()
