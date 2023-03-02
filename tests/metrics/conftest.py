import pytest

from mlserver.server import MLServer
from mlserver.settings import Settings
from mlserver.metrics.prometheus import PrometheusEndpoint

from .utils import MetricsClient


@pytest.fixture
def prometheus_endpoint(settings: Settings) -> PrometheusEndpoint:
    return PrometheusEndpoint(settings)


@pytest.fixture
async def metrics_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.metrics_port}"
    client = MetricsClient(http_server, metrics_endpoint=settings.metrics_endpoint)

    yield client

    await client.close()
