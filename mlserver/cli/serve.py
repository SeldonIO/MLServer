import os
import importlib
import sys

from typing import Type

from ..server import MLServer
from ..model import MLModel
from ..settings import Settings, ModelSettings

DEFAULT_SETTINGS_FILENAME = "settings.json"
DEFAULT_MODEL_SETTINGS_FILENAME = "model-settings.json"


def init_mlserver(folder: str) -> MLServer:
    """
    Instantiate a MLServer instance from a folder's config.
    """
    model_settings_path = os.path.join(folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    model_settings = ModelSettings.parse_file(model_settings_path)

    model_object = _init_model(model_settings)

    settings_path = os.path.join(folder, DEFAULT_SETTINGS_FILENAME)
    settings = Settings.parse_file(settings_path)

    return MLServer(settings, models=[model_object])


def _init_model(model_settings: ModelSettings) -> MLModel:
    model_class = _import_model(model_settings.implementation)
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
