import os
import pytest
import shutil
import docker

from docker.client import DockerClient

from ..conftest import TESTDATA_PATH


@pytest.fixture
def custom_runtime_path(model_folder: str) -> str:
    to_copy = ["models.py", "environment.yml"]
    for file_name in to_copy:
        src = os.path.join(TESTDATA_PATH, file_name)
        dst = os.path.join(model_folder, file_name)
        shutil.copyfile(src, dst)

    return model_folder


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()
