"""
Command-line interface to manage MLServer models.
"""
import click
import importlib
import sys

from typing import Type

from ..server import MLServer
from ..model import MLModel
from ..settings import Settings, ModelSettings

from .build import generate_bundle


@click.group()
@click.version_option()
def root():
    """
    Command-line interface to manage MLServer models.
    """
    pass


@root.command("bundle")
@click.argument("folder")
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


@root.command("serve")
@click.argument("model", nargs=1)
@click.option(
    "--model-settings",
    type=click.Path(exists=True),
    required=True,
    help="Model settings to load",
)
@click.option("--debug/--production", default=False, help="Run in debug mode")
@click.option("--http_port", type=int, help="Port for the HTTP server")
@click.option("--grpc_port", type=int, help="Port for the gRPC server")
def serve(model: str, model_settings: str, debug: bool, http_port: int, grpc_port: int):
    """
    Start serving a machine learning model with MLServer.
    """
    model_object = _instantiate_model(
        model_module=model, model_settings_path=model_settings
    )

    settings = Settings(debug=debug)

    if http_port is not None:
        settings.http_port = http_port

    if grpc_port is not None:
        settings.grpc_port = grpc_port

    server = MLServer(settings, models=[model_object])
    server.start()


def _instantiate_model(model_module: str, model_settings_path: str) -> MLModel:
    model_class = _import_model(model_module)
    model_settings = ModelSettings.parse_file(model_settings_path)

    return model_class(model_settings)


def _import_model(model_module: str) -> Type[MLModel]:
    # NOTE: Insert current directory into syspath to load specified model.
    # TODO: Make model-dir configurable.
    sys.path.insert(0, ".")

    model_package, model_class_name = model_module.rsplit(".", 1)

    module = importlib.import_module(model_package)
    model_class = getattr(module, model_class_name)

    # TODO: Validate that `model_class` is a subtype of MLModel
    return model_class


def main():
    root()


if __name__ == "__main__":
    main()
