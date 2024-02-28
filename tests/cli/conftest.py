import pytest
import docker
import logging

from typing import Tuple
from docker.client import DockerClient

from ..utils import get_available_ports

logger = logging.getLogger()


@pytest.fixture(scope="module")
def docker_client() -> DockerClient:
    logger.debug("Docker client: starting")
    client = docker.from_env()
    logger.debug("Docker client: started")

    logger.debug("Docker client: yielding")
    yield client
    logger.debug("Docker client: yielded")

    logger.debug("Docker client: closing")
    client.close()
    logger.debug("Docker client: closed")


@pytest.fixture
def free_ports() -> Tuple[int, int, int]:
    http_port, grpc_port, metrics_port = get_available_ports(3)
    return http_port, grpc_port, metrics_port
