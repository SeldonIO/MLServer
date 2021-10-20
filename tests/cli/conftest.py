import pytest
import docker

from docker.client import DockerClient


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()
