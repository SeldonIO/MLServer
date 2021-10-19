import os

from docker.client import DockerClient

from mlserver import __version__
from mlserver.cli.constants import DockerfileTemplate
from mlserver.cli.build import generate_dockerfile


def test_generate_dockerfile():
    default_runtime = "my_custom_runtime"
    dockerfile = generate_dockerfile(default_runtime=default_runtime)

    assert dockerfile == DockerfileTemplate.format(
        version=__version__, default_runtime=default_runtime
    )


def test_build(docker_client: DockerClient, custom_image: str):
    image = docker_client.images.get(custom_image)
    assert image.tags == [custom_image]
