"""
Command-line interface to manage MLServer models.
"""
import click
import asyncio

from functools import wraps

from ..server import MLServer
from ..logging import logger, configure_logger
from ..utils import install_uvloop_event_loop

from .build import generate_dockerfile, build_image, write_dockerfile
from .serve import load_settings


def click_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
@click.version_option()
def root():
    """
    Command-line interface to manage MLServer models.
    """
    pass


@root.command("start")
@click.argument("folder", nargs=1)
@click_async
async def start(folder: str):
    """
    Start serving a machine learning model with MLServer.
    """
    settings, models_settings = await load_settings(folder)

    server = MLServer(settings)
    await server.start(models_settings)


@root.command("build")
@click.argument("folder", nargs=1)
@click.option("-t", "--tag", type=str)
@click_async
async def build(folder: str, tag: str):
    """
    Build a Docker image for a custom MLServer runtime.
    """
    dockerfile = generate_dockerfile()
    build_image(folder, dockerfile, tag)
    logger.info(f"Successfully built custom Docker image with tag {tag}")


@root.command("dockerfile")
@click.argument("folder", nargs=1)
@click.option("-i", "--include-dockerignore", is_flag=True)
@click_async
async def dockerfile(folder: str, include_dockerignore: bool):
    """
    Generate a Dockerfile
    """
    dockerfile = generate_dockerfile()
    dockerfile_path = write_dockerfile(
        folder, dockerfile, include_dockerignore=include_dockerignore
    )
    logger.info(f"Successfully written Dockerfile in {dockerfile_path}")


def main():
    configure_logger()
    install_uvloop_event_loop()
    root()


if __name__ == "__main__":
    main()
