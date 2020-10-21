import os
import sys
import glob

from typing import List, Tuple, Union

from ..model import MLModel
from ..settings import Settings, ModelParameters, ModelSettings

DEFAULT_SETTINGS_FILENAME = "settings.json"
DEFAULT_MODEL_SETTINGS_FILENAME = "model-settings.json"


def load_settings(folder: str = None) -> Tuple[Settings, List[MLModel]]:
    """
    Load server and model settings.
    """
    # NOTE: Insert current directory and model folder into syspath to load
    # specified model.
    sys.path.insert(0, ".")

    if folder:
        sys.path.insert(0, folder)

    settings = None
    if _path_exists(folder, DEFAULT_SETTINGS_FILENAME):
        settings_path = os.path.join(folder, DEFAULT_SETTINGS_FILENAME)  # type: ignore
        settings = Settings.parse_file(settings_path)
    else:
        settings = Settings()

    models = _load_models(folder)

    return settings, models


def _load_models(folder: str = None) -> List[MLModel]:
    model_objects = []

    if folder:
        pattern = os.path.join(folder, "**", DEFAULT_MODEL_SETTINGS_FILENAME)
        matches = glob.glob(pattern, recursive=True)

        for model_settings_path in matches:
            model_settings = _load_model_settings(model_settings_path)
            model_object = _init_model(model_settings)
            model_objects.append(model_object)

    # If there were no matches, try to load model from environment
    if not model_objects:
        model_settings = ModelSettings()
        model_settings.parameters = ModelParameters()
        model_object = _init_model(model_settings)
        model_objects.append(model_object)

    return model_objects


def _load_model_settings(model_settings_path: str) -> ModelSettings:
    model_settings = ModelSettings.parse_file(model_settings_path)

    if not model_settings.parameters:
        # If not specified, default to its own folder
        default_model_uri = os.path.dirname(model_settings_path)
        model_settings.parameters = ModelParameters(uri=default_model_uri)

    return model_settings


def _path_exists(folder: Union[str, None], file: str) -> bool:
    if folder is None:
        return False

    file_path = os.path.join(folder, file)
    return os.path.isfile(file_path)


def _init_model(model_settings: ModelSettings) -> MLModel:
    model_class = model_settings.implementation
    return model_class(model_settings)  # type: ignore
