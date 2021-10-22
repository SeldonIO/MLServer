import os
import pytest

from docker.client import DockerClient
from pytest_cases import fixture, parametrize_with_cases
from typing import Tuple

from mlserver import __version__
from mlserver.types import InferenceRequest
from mlserver.settings import Settings, ModelSettings
from mlserver.cli.constants import DockerfileTemplate
from mlserver.cli.build import generate_dockerfile, build_image


@fixture
@parametrize_with_cases("custom_runtime_path")
def custom_image(
    docker_client: DockerClient, custom_runtime_path: str, current_cases
) -> str:
    dockerfile = generate_dockerfile()
    current_case = current_cases["custom_image"]["custom_runtime_path"]
    image_name = f"{current_case.id}:0.1.0"
    build_image(custom_runtime_path, dockerfile, image_name)

    yield image_name

    docker_client.images.remove(image=image_name, force=True)


@pytest.fixture
def custom_runtime_server(
    docker_client: DockerClient,
    custom_image: str,
    settings: Settings,
    free_ports: Tuple[str, str],
) -> str:
    host_http_port, host_grpc_port = free_ports

    breakpoint()
    container = docker_client.containers.run(
        custom_image,
        ports={
            f"{settings.http_port}/tcp": host_http_port,
            f"{settings.grpc_port}/tcp": host_grpc_port,
        },
    )

    yield f"127.0.0.1:{host_http_port}", f"127.0.0.1:{host_grpc_port}"

    container.remove(force=True)


def test_generate_dockerfile():
    dockerfile = generate_dockerfile()

    assert dockerfile == DockerfileTemplate.format(version=__version__)


def test_build(docker_client: DockerClient, custom_image: str):
    image = docker_client.images.get(custom_image)
    assert image.tags == [custom_image]


async def test_infer_custom_runtime(
    docker_client: DockerClient,
    custom_runtime_server: Tuple[str, str],
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    http_server, _ = custom_runtime
    endpoint = f"{http_server}/v2/models/{sum_model_settings.name}/infer"
    breakpoint()
    response = await aiohttp.post(endpoint, json=inference_request.dict())
