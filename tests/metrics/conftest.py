import pytest
import asyncio

from mlserver.server import MLServer
from mlserver.settings import Settings, ModelSettings

from ..utils import RESTClient, get_available_ports
from .utils import MetricsClient


@pytest.fixture
def settings(settings: Settings) -> Settings:
    http_port, grpc_port, metrics_port = get_available_ports(3)
    settings.http_port = http_port
    settings.grpc_port = grpc_port
    settings.metrics_port = metrics_port

    return settings


@pytest.fixture
async def mlserver(
    settings: Settings,
    sum_model_settings: ModelSettings,
):
    server = MLServer(settings)

    # Start server without blocking, and cancel afterwards
    server_task = asyncio.create_task(server.start())

    # Load sample model
    await server._model_registry.load(sum_model_settings)

    yield server

    await server.stop()
    await server_task


@pytest.fixture
async def metrics_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.metrics_port}"
    client = MetricsClient(http_server, metrics_endpoint=settings.metrics_endpoint)

    yield client

    await client.close()


@pytest.fixture
async def rest_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    client = RESTClient(http_server)

    yield client

    await client.close()
