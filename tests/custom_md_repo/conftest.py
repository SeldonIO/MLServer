import os
import pytest
import asyncio

from prometheus_client.registry import REGISTRY, CollectorRegistry
from starlette_exporter import PrometheusMiddleware

from mlserver.server import MLServer
from mlserver.settings import Settings, ModelSettings

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")

from ..utils import RESTClient, get_available_ports


@pytest.fixture()
def prometheus_registry() -> CollectorRegistry:
    """
    Fixture used to ensure the registry is cleaned on each run.
    Otherwise, `py-grpc-prometheus` will complain that metrics already exist.

    TODO: Open issue in `py-grpc-prometheus` to check whether a metric exists
    before creating it.
    For an example on how to do this, see `starlette_exporter`'s implementation

        https://github.com/stephenhillier/starlette_exporter/blob/947d4d631dd9a6a8c1071b45573c5562acba4834/starlette_exporter/middleware.py#L67
    """
    # NOTE: Since the `REGISTRY` object is global, this fixture is NOT
    # thread-safe!!
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)

    # Clean metrics from `starlette_exporter` as well, as otherwise they won't
    # get re-created
    PrometheusMiddleware._metrics.clear()

    yield REGISTRY


@pytest.fixture
def settings() -> Settings:
    settings_path = os.path.join(TESTDATA_PATH, "settings-custom-md-repo.json")
    return Settings.parse_file(settings_path)


@pytest.fixture
async def mlserver(
    settings: Settings,
    sum_model_settings: ModelSettings,
    prometheus_registry: CollectorRegistry,  # noqa: F811
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
async def rest_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    client = RESTClient(http_server)

    yield client

    await client.close()
