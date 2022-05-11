import os
import pytest
import shutil
import signal
import json

from aiohttp.client_exceptions import ClientResponseError
from subprocess import Popen
from typing import Tuple

from mlserver.cli.serve import DEFAULT_SETTINGS_FILENAME
from mlserver.repository import DEFAULT_MODEL_SETTINGS_FILENAME
from mlserver.settings import ModelSettings, Settings
from mlserver.types import InferenceRequest

from ..conftest import TESTDATA_PATH
from ..utils import RESTClient


@pytest.fixture
def settings(settings: Settings, free_ports: Tuple[int, int]) -> Settings:
    http_port, grpc_port = free_ports

    settings.http_port = http_port
    settings.grpc_port = grpc_port

    return settings


@pytest.fixture
def mlserver_folder(tmp_path: str, settings: Settings) -> str:
    """
    This fixture should create an MLServer folder with some base settings and
    two models: a copy of the standard SumModel, as well as a copy of the
    SlowModel.
    """
    # Write settings.json with free ports
    settings_path = os.path.join(tmp_path, DEFAULT_SETTINGS_FILENAME)
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings.json())

    # Copy models.py module
    src_path = os.path.join(TESTDATA_PATH, "models.py")
    dst_path = os.path.join(tmp_path, "models.py")
    shutil.copy(src_path, dst_path)

    # Copy SumModel's model-settings.json
    sum_model_folder = os.path.join(tmp_path, "sum-model")
    os.makedirs(sum_model_folder)
    old_path = os.path.join(TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME)
    new_path = os.path.join(sum_model_folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    shutil.copy(old_path, new_path)

    # Write SlowModel's model-settings.json
    slow_model_folder = os.path.join(tmp_path, "slow-model")
    os.makedirs(slow_model_folder)
    slow_model_settings_path = os.path.join(
        slow_model_folder, DEFAULT_MODEL_SETTINGS_FILENAME
    )
    with open(slow_model_settings_path, "w") as slow_model_file:
        slow_model_settings = {
            "name": "slow-model",
            "implementation": "models.SlowModel",
        }
        slow_model_file.write(json.dumps(slow_model_settings))

    return tmp_path


@pytest.fixture
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
