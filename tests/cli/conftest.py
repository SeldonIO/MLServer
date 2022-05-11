import pytest
import docker
import os
import signal
import shutil
import json


from typing import Tuple
from docker.client import DockerClient
from subprocess import Popen

from mlserver.settings import Settings, ModelSettings
from mlserver.cli.serve import DEFAULT_SETTINGS_FILENAME
from mlserver.cli.main import start
from mlserver.repository import DEFAULT_MODEL_SETTINGS_FILENAME

from ..utils import get_available_port, RESTClient
from ..conftest import TESTDATA_PATH


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture
def free_ports() -> Tuple[int, int]:
    http_port = get_available_port()
    grpc_port = get_available_port()
    return http_port, grpc_port


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
    cmd = f"mlserver start {mlserver_folder}"
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
