import pytest
import asyncio

from tempfile import TemporaryDirectory
from prometheus_client.registry import REGISTRY, CollectorRegistry
from starlette_exporter import PrometheusMiddleware

from mlserver.server import MLServer
from mlserver.settings import Settings, ModelSettings

from ..utils import RESTClient, get_available_ports

import os
from ..conftest import TESTDATA_PATH


@pytest.fixture()
def tmp_dir():
    directory = TemporaryDirectory()
    yield directory
    directory.cleanup()


@pytest.fixture()
def single_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "single.txt")


@pytest.fixture()
def invalid_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "invalid.txt")


@pytest.fixture()
def invalid_among_many():
    return os.path.join(TESTDATA_PATH, "batch_processing", "invalid_among_many.txt")


@pytest.fixture()
def many_input():
    return os.path.join(TESTDATA_PATH, "batch_processing", "many.txt")

@pytest.fixture()
def single_input_with_id():
    return os.path.join(TESTDATA_PATH, "batch_processing", "single_with_id.txt")


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
