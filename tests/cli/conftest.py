import pytest
import docker
import socket

from typing import Tuple
from docker.client import DockerClient


def _get_available_port() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return str(port)


@pytest.fixture
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture
def free_ports() -> Tuple[str, str]:
    http_port = _get_available_port()
    grpc_port = _get_available_port()
    return http_port, grpc_port
