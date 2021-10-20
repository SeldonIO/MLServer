import os

from docker.client import DockerClient
from pytest_cases import fixture, parametrize_with_cases

from mlserver import __version__
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


def test_generate_dockerfile():
    default_runtime = "my_custom_runtime"
    dockerfile = generate_dockerfile(default_runtime=default_runtime)

    assert dockerfile == DockerfileTemplate.format(
        version=__version__, default_runtime=default_runtime
    )


def test_build(docker_client: DockerClient, custom_image: str):
    image = docker_client.images.get(custom_image)
    assert image.tags == [custom_image]
