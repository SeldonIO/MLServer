"""
Command-line interface to manage MLServer models.
"""
import click

from .build import generate_bundle
from .serve import init_mlserver


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
async def start(folder: str):
    """
    Start serving a machine learning model with MLServer.
    """
    server = await init_mlserver(folder)
    server.start()


def main():
    root()


if __name__ == "__main__":
    main()
