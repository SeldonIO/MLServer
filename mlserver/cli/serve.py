import os
import importlib
import sys

from typing import Type, List

from ..model import MLModel
from ..settings import Settings, ModelSettings

DEFAULT_SETTINGS_FILENAME = "settings.json"
DEFAULT_MODEL_SETTINGS_FILENAME = "model-settings.json"


def read_folder(folder: str) -> (Settings, List[MLModel]):
    """
    Read a folder's config.
    """
    # NOTE: Insert current directory and model folder into syspath to load
    # specified model.
    sys.path.insert(0, ".")
    sys.path.insert(0, folder)

    settings_path = os.path.join(folder, DEFAULT_SETTINGS_FILENAME)
    settings = Settings.parse_file(settings_path)

    model_settings_path = os.path.join(folder, DEFAULT_MODEL_SETTINGS_FILENAME)
    model_settings = ModelSettings.parse_file(model_settings_path)

    model_object = _init_model(model_settings)

    return settings, [model_object]


def _init_model(model_settings: ModelSettings) -> MLModel:
    model_class = _import_model(model_settings.implementation)
    return model_class(model_settings)


def _import_model(model_module: str) -> Type[MLModel]:
    model_package, model_class_name = model_module.rsplit(".", 1)

    module = importlib.import_module(model_package)
    model_class = getattr(module, model_class_name)

    # TODO: Validate that `model_class` is a subtype of MLModel
    return model_class
