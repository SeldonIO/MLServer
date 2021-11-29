import pytest
import asyncio

from prometheus_client.registry import CollectorRegistry

from mlserver.server import MLServer
from mlserver.settings import Settings
from mlserver.model import MLModel

from ..grpc.conftest import prometheus_registry  # noqa: F401
from ..utils import get_available_port
from .utils import MetricsClient


@pytest.fixture
def settings(settings: Settings) -> Settings:
    settings.http_port = get_available_port()
    settings.grpc_port = get_available_port()

    return settings


@pytest.fixture
async def mlserver(
    settings: Settings,
    sum_model: MLModel,
    prometheus_registry: CollectorRegistry,  # noqa: F811
):
    server = MLServer(settings)

    # Start server without blocking, and cancel afterwards
    loop = asyncio.get_event_loop()
    server_task = loop.create_task(server.start())

    # Load sample model
    await server._model_registry.load(sum_model)

    yield server

    server_task.cancel()

    try:
        # Ignore error from cancelling server task
        await server_task
        await server.stop()
    except Exception:
        pass


@pytest.fixture
async def metrics_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    return MetricsClient(http_server)
