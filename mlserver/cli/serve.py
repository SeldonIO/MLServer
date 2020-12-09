import os
import sys

from typing import List, Tuple, Union

from ..model import MLModel
from ..repository import ModelRepository
from ..settings import Settings, ModelSettings

DEFAULT_SETTINGS_FILENAME = "settings.json"


async def load_settings(folder: str = None) -> Tuple[Settings, List[MLModel]]:
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

    if folder is not None:
        settings.model_repository_root = folder

    models = []
    if settings.load_models_at_startup:
        repository = ModelRepository(settings.model_repository_root)
        available_models = await repository.list()
        models = [_init_model(model) for model in available_models]

    return settings, models


def _path_exists(folder: Union[str, None], file: str) -> bool:
    if folder is None:
        return False

    file_path = os.path.join(folder, file)
    return os.path.isfile(file_path)


def _init_model(model_settings: ModelSettings) -> MLModel:
    model_class = model_settings.implementation
    return model_class(model_settings)  # type: ignore
