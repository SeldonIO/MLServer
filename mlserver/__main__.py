"""
Starts an inference server.
"""
import click
import importlib

from typing import Type

from .server import MLServer
from .model import MLModel
from .settings import Settings, ModelSettings


def _instantiate_model(model_module: str, model_settings_path: str) -> MLModel:
    model_class = _import_model(model_module)

    model_settings = None
    with open(model_settings_path) as model_settings_file:
        json_content = model_settings_file.read()
        model_settings = ModelSettings.parse_raw(json_content)

    return model_class(model_settings)


def _import_model(model_module: str) -> Type[MLModel]:
    model_package, model_class_name = model_module.rsplit(".", 1)

    module = importlib.import_module(model_package)
    model_class = getattr(module, model_class_name)

    # TODO: Validate that `model_class` is a subtype of MLModel
    return model_class


@click.command("serve", help="Start serving a machine learning model")
@click.argument("model", nargs=1)
@click.option(
    "--model-settings", type=click.Path(exists=True), help="Model settings to load"
)
def serve(model: str, model_settings: str):
    model_object = _instantiate_model(
        model_module=model, model_settings_path=model_settings
    )
    settings = Settings()

    server = MLServer(settings, models=[model_object])
    server.start()


if __name__ == "__main__":
    serve()
