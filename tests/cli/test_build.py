import logging

import pytest
import random

from docker.client import DockerClient
from pytest_cases import fixture, parametrize_with_cases
from typing import Tuple, Optional

from mlserver import __version__
from mlserver.types import InferenceRequest, Parameters
from mlserver.settings import Settings
from mlserver.cli.constants import DockerfileTemplate, DefaultBaseImage
from mlserver.cli.build import generate_dockerfile, build_image

from ..utils import RESTClient


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

    # in CI sometimes this fails, TODO: indentify why
    try:
        docker_client.images.remove(image=image_name, force=True)
    except Exception:
        logging.warning("skipping remove")


@pytest.fixture
def random_user_id() -> int:
    return random.randint(1000, 65536)


@pytest.fixture
def custom_runtime_server(
    docker_client: DockerClient,
    custom_image: str,
    settings: Settings,
    free_ports: Tuple[int, int, int],
    random_user_id: int,
) -> str:
    host_http_port, host_grpc_port, host_metrics_port = free_ports

    container = docker_client.containers.run(
        custom_image,
        ports={
            f"{settings.http_port}/tcp": str(host_http_port),
            f"{settings.grpc_port}/tcp": str(host_grpc_port),
            f"{settings.metrics_port}/tcp": str(host_metrics_port),
        },
        detach=True,
        user=random_user_id,
    )

    yield f"127.0.0.1:{host_http_port}", f"127.0.0.1:{host_grpc_port}"

    container.remove(force=True)


@pytest.mark.parametrize(
    "base_image",
    [
        None,
        "customreg/customimage:{version}-slim",
        "customreg/custonimage:customtag",
    ],
)
def test_generate_dockerfile(base_image: Optional[str]):
    dockerfile = ""
    if base_image is None:
        dockerfile = generate_dockerfile()
        base_image = DefaultBaseImage
    else:
        dockerfile = generate_dockerfile(base_image=base_image)

    expected = base_image.format(version=__version__)
    assert expected in dockerfile
    assert dockerfile == DockerfileTemplate.format(base_image=expected)


def test_build(docker_client: DockerClient, custom_image: str):
    image = docker_client.images.get(custom_image)
    assert image.tags == [custom_image]


async def test_infer_custom_runtime(
    custom_runtime_server: Tuple[str, str],
    inference_request: InferenceRequest,
):
    http_server, _ = custom_runtime_server
    rest_client = RESTClient(http_server)
    await rest_client.wait_until_ready()

    loaded_models = await rest_client.list_models()
    assert len(loaded_models) == 1

    model_name = loaded_models[0].name
    inference_request.inputs[0].parameters = Parameters(content_type="np")
    inference_response = await rest_client.infer(model_name, inference_request)
    assert len(inference_response.outputs) == 1

    await rest_client.close()
