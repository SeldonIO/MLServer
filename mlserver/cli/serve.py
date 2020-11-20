import os
import sys

from typing import List, Tuple, Union

from ..model import MLModel
from ..loader import ModelSettingsLoader
from ..settings import Settings, ModelSettings

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

    model_settings_loader = ModelSettingsLoader(folder)
    models = [_init_model(model) for model in model_settings_loader.list()]

    return settings, models


def _path_exists(folder: Union[str, None], file: str) -> bool:
    if folder is None:
        return False

    file_path = os.path.join(folder, file)
    return os.path.isfile(file_path)


def _init_model(model_settings: ModelSettings) -> MLModel:
    model_class = model_settings.implementation
    return model_class(model_settings)  # type: ignore
