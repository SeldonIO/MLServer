import pytest
import asyncio

from typing import List

from prometheus_client import Metric
from prometheus_client.parser import text_string_to_metric_families
from mlserver.server import MLServer
from mlserver.settings import Settings

from ..utils import RESTClient, get_available_port


class MetricsClient(RESTClient):
    async def metrics(self) -> List[Metric]:
        endpoint = f"http://{self._http_server}/metrics"
        response = await self._session.get(endpoint)

        raw_metrics = await response.text()
        return text_string_to_metric_families(raw_metrics)


@pytest.fixture
def settings(settings: Settings) -> Settings:
    settings.http_port = get_available_port()
    settings.grpc_port = get_available_port()

    return settings


@pytest.fixture
async def mlserver(settings: Settings):
    server = MLServer(settings)

    # Start server without blocking, and cancel afterwards
    loop = asyncio.get_event_loop()
    server_task = loop.create_task(server.start())

    yield server

    server_task.cancel()

    try:
        # Ignore error from cancelling server task
        await server_task
        await server.stop()
    except Exception:
        pass


@pytest.fixture
async def rest_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    return RESTClient(http_server)


@pytest.fixture
async def metrics_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    return MetricsClient(http_server)
