import pytest
import docker

from typing import Tuple
from docker.client import DockerClient

from ..utils import get_available_port


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture
def free_ports() -> Tuple[int, int]:
    http_port = get_available_port()
    grpc_port = get_available_port()
    metrics_port = get_available_port()
    return http_port, grpc_port, metrics_port
