import pytest
import docker
import os

from typing import Tuple
from docker.client import DockerClient

from mlserver.settings import Settings, ModelSettings

from ..utils import get_available_port


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture
def free_ports() -> Tuple[int, int]:
    http_port = get_available_port()
    grpc_port = get_available_port()
    return http_port, grpc_port
