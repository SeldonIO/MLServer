import subprocess
import os

from tempfile import TemporaryDirectory

from .. import __version__
from ..logging import logger

from .constants import (
    DockerfileName,
    DockerfileTemplate,
    DockerignoreName,
    Dockerignore,
)


def generate_dockerfile() -> str:
    return DockerfileTemplate.format(version=__version__)


def write_dockerfile(
    folder: str, dockerfile: str, include_dockerignore: bool = True
) -> str:
    dockerfile_path = os.path.join(folder, DockerfileName)
    with open(dockerfile_path, "w") as dockerfile_handler:
        logger.info(f"Writing Dockerfile in {dockerfile_path}")
        dockerfile_handler.write(dockerfile)

    if include_dockerignore:
        # Point to our own .dockerignore
        # https://docs.docker.com/engine/reference/commandline/build/#use-a-dockerignore-file
        dockerignore_path = dockerfile_path + DockerignoreName
        with open(dockerignore_path, "w") as dockerignore_handler:
            logger.info(f"Writing .dockerignore in {dockerignore_path}")
            dockerignore_handler.write(Dockerignore)

    return dockerfile_path


def build_image(
    folder: str, dockerfile: str, image_tag: str, no_cache: bool = False
) -> str:
    logger.info(f"Building Docker image with tag {image_tag}")
    _docker_command_prefix = "docker build --rm "
    with TemporaryDirectory() as tmp_dir:
        dockerfile_path = write_dockerfile(tmp_dir, dockerfile)
        _docker_command_suffix = f"{folder} -f {dockerfile_path} -t {image_tag}"
        if no_cache:
            build_cmd = _docker_command_prefix + "--no-cache " + _docker_command_suffix
        else:
            build_cmd = _docker_command_prefix + _docker_command_suffix
        build_env = os.environ.copy()
        build_env["DOCKER_BUILDKIT"] = "1"
        subprocess.run(build_cmd, check=True, shell=True, env=build_env)

    return image_tag
