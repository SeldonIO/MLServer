import subprocess
import os

from typing import Tuple
from tempfile import TemporaryDirectory

from .. import __version__
from .constants import (
    DockerfileName,
    DockerfileTemplate,
    DockerignoreName,
    Dockerignore,
)


def generate_dockerfile(default_runtime: str = "") -> str:
    return DockerfileTemplate.format(version=__version__, default_runtime="")


def write_dockerfile(folder: str, dockerfile: str) -> str:
    dockerfile_path = os.path.join(folder, DockerfileName)
    with open(dockerfile_path, "w") as dockerfile_handler:
        dockerfile_handler.write(dockerfile)

    # Point to our own .dockerignore
    # https://docs.docker.com/engine/reference/commandline/build/#use-a-dockerignore-file
    dockerignore_path = dockerfile_path + DockerignoreName
    with open(dockerignore_path, "w") as dockerignore_handler:
        dockerignore_handler.write(Dockerignore)

    return dockerfile_path


def build_image(folder: str, dockerfile: str, image_tag: str) -> str:
    with TemporaryDirectory() as tmp_dir:
        dockerfile_path = write_dockerfile(tmp_dir, dockerfile)

        build_cmd = f"docker build {folder} -f {dockerfile_path} -t {image_tag}"
        build_env = {"DOCKER_BUILDKIT": "1"}
        subprocess.run(build_cmd, check=True, shell=True, env=build_env)

    return image_tag
