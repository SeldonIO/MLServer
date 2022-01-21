import os
import sys

from typing import List, Tuple, Union

from ..repository import ModelRepository
from ..settings import Settings, ModelSettings

DEFAULT_SETTINGS_FILENAME = "settings.json"


async def load_settings(folder: str = None) -> Tuple[Settings, List[ModelSettings]]:
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

    models_settings = []
    if settings.load_models_at_startup:
        repository = ModelRepository(settings.model_repository_root)
        models_settings = await repository.list()

    return settings, models_settings


def _path_exists(folder: Union[str, None], file: str) -> bool:
    if folder is None:
        return False

    file_path = os.path.join(folder, file)
    return os.path.isfile(file_path)
