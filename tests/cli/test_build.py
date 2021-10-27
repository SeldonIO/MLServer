import os
import pytest

from docker.client import DockerClient
from pytest_cases import fixture, parametrize_with_cases
from typing import Tuple

from mlserver import __version__
from mlserver.types import InferenceRequest, Parameters
from mlserver.settings import Settings, ModelSettings
from mlserver.cli.constants import DockerfileTemplate
from mlserver.cli.build import generate_dockerfile, build_image

from .utils import APIClient


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

    container = docker_client.containers.run(
        custom_image,
        ports={
            f"{settings.http_port}/tcp": host_http_port,
            f"{settings.grpc_port}/tcp": host_grpc_port,
        },
        detach=True,
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
    custom_runtime_server: Tuple[str, str],
    inference_request: InferenceRequest,
):
    http_server, _ = custom_runtime_server
    api_client = APIClient(http_server)
    await api_client.wait_until_ready()

    loaded_models = await api_client.list_models()
    assert len(loaded_models) == 1

    model_name = loaded_models[0].name
    inference_request.inputs[0].parameters = Parameters(content_type="np")
    inference_response = await api_client.infer(model_name, inference_request)
    assert len(inference_response.outputs) == 1

    api_client.close()
