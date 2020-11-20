"""
Command-line interface to manage MLServer models.
"""
import click
import asyncio

from functools import wraps

from ..server import MLServer

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
    settings, models = await load_settings(folder)

    server = MLServer(settings)
    await server.start(models)


def main():
    root()


if __name__ == "__main__":
    main()
