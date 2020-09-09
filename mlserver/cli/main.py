"""
Command-line interface to manage MLServer models.
"""
import click
import asyncio

from functools import wraps

from ..server import MLServer

from .build import generate_bundle
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


@root.command("bundle")
@click.argument("folder", nargs=1)
def bundle(folder: str):
    """
    Generates a bundle which can be used to build a Docker image to serve a
    machine learning model.

    Parameters
    -----
    folder : str
        Folder containing your model server code and config.
    """
    generate_bundle(folder)


@root.command("start")
@click.argument("folder", nargs=1)
@click_async
async def start(folder: str):
    """
    Start serving a machine learning model with MLServer.
    """
    settings, models = load_settings(folder)

    server = MLServer(settings)
    await server.start(models)


def main():
    root()


if __name__ == "__main__":
    main()
