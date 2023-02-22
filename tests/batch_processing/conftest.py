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
