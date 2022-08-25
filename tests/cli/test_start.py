import os
import pytest
import signal

from aiohttp.client_exceptions import ClientResponseError
from subprocess import Popen
from typing import Tuple
from pytest_cases import fixture, parametrize_with_cases

from mlserver.settings import ModelSettings, Settings
from mlserver.types import InferenceRequest

from ..utils import RESTClient


@pytest.fixture
def settings(settings: Settings, free_ports: Tuple[int, int]) -> Settings:
    http_port, grpc_port, metrics_port = free_ports

    settings.http_port = http_port
    settings.grpc_port = grpc_port
    settings.metrics_port = metrics_port

    return settings


@fixture
@parametrize_with_cases("mlserver_folder")
def mlserver_start(mlserver_folder: str) -> Popen:
    p = Popen(["mlserver", "start", mlserver_folder], start_new_session=True)

    yield p

    os.killpg(os.getpgid(p.pid), signal.SIGTERM)


@pytest.fixture
async def rest_client(settings: Settings, mlserver_start) -> RESTClient:
    http_server = f"127.0.0.1:{settings.http_port}"
    client = RESTClient(http_server)
    await client.wait_until_live()

    yield client

    await client.close()


async def test_live(rest_client: RESTClient):
    is_live = await rest_client.live()
    assert is_live

    # Assert that the server is live, but some models are still loading
    with pytest.raises(ClientResponseError):
        await rest_client.ready()


async def test_infer(
    rest_client: RESTClient,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    await rest_client.wait_until_model_ready(sum_model_settings.name)
    response = await rest_client.infer(sum_model_settings.name, inference_request)

    assert len(response.outputs) == 1
