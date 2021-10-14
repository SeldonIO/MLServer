import os

from docker.client import DockerClient

from mlserver import __version__
from mlserver.cli.build import generate_dockerfile, Dockerignore, DockerfileTemplate


def test_generate_dockerfile():
    source_folder = "."
    dockerfile, dockerignore = generate_dockerfile(source_folder)

    assert dockerignore == Dockerignore
    assert dockerfile == DockerfileTemplate.format(
        version=__version__, default_runtime="", source_folder=source_folder
    )


def test_valid_dockerfile(docker_client: DockerClient, custom_runtime_path: str):
    dockerfile, dockerignore = generate_dockerfile(custom_runtime_path)

    # TODO: (needs to change) Copy Dockerfile to path
    dockerfile_path = os.path.join(custom_runtime_path, "Dockerfile")
    with open(dockerfile_path, "w") as file:
        file.write(dockerfile)

    # TODO: (needs to change) Copy .dockerignore to path
    dockerignore_path = os.path.join(custom_runtime_path, ".dockerignore")
    with open(dockerignore_path, "w") as file:
        file.write(dockerignore)

    breakpoint()
    image = docker_client.images.build(
        path=str(custom_runtime_path), dockerfile=dockerfile_path
    )
    breakpoint()
    assert True
