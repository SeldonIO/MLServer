import os
import sys

from typing import List

from ..model import MLModel
from ..settings import Settings, ModelParameters, ModelSettings

DEFAULT_SETTINGS_FILENAME = "settings.json"
DEFAULT_MODEL_SETTINGS_FILENAME = "model-settings.json"


def load_settings(folder: str) -> (Settings, List[MLModel]):
    """
    Load server and model settings.
    """
    # NOTE: Insert current directory and model folder into syspath to load
    # specified model.
    sys.path.insert(0, ".")
    sys.path.insert(0, folder)

    settings_path = os.path.join(folder, DEFAULT_SETTINGS_FILENAME)

    settings = None
    if os.path.isfile(settings_path):
        settings = Settings.parse_file(settings_path)
    else:
        settings = Settings()

    models = _load_models(folder)

    return settings, models


def _load_models(folder: str) -> List[MLModel]:
    model_settings_path = os.path.join(folder, DEFAULT_MODEL_SETTINGS_FILENAME)

    model_settings = None
    if os.path.isfile(model_settings_path):
        model_settings = ModelSettings.parse_file(model_settings_path)
    else:
        model_settings = ModelSettings()
        model_settings.parameters = ModelParameters()

    model_object = _init_model(model_settings)

    return [model_object]


def _init_model(model_settings: ModelSettings) -> MLModel:
    model_class = model_settings.implementation
    return model_class(model_settings)
