import os
import pytest
import shutil
import docker

from docker.client import DockerClient

from mlserver.cli.build import generate_dockerfile, build_image

from ..conftest import TESTDATA_PATH

CustomImageTag = "test/my-custom-image:0.1.0"


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


@pytest.fixture
def custom_image(docker_client: DockerClient, custom_runtime_path: str) -> str:
    dockerfile = generate_dockerfile()
    build_image(custom_runtime_path, dockerfile, CustomImageTag)

    yield CustomImageTag

    docker_client.images.remove(image=CustomImageTag, force=True)
