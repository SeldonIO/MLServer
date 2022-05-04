import os
import sys
import asyncio

from typing import List, Tuple, Union

from ..repository import ModelRepository
from ..settings import Settings, ModelSettings
from ..logging import logger

DEFAULT_SETTINGS_FILENAME = "settings.json"


def load_server_settings(folder: str = None) -> Settings:
    """
    Load server settings.
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

    return settings


async def load_settings(
    folder: str = None, server_settings: Settings = None
) -> Tuple[Settings, List[ModelSettings]]:
    """
    Load server and model settings.
    """
    settings = server_settings
    if not settings:
        settings = load_server_settings(folder)

    if folder is not None:
        settings.model_repository_root = folder

    models_settings = []
    if settings.load_models_at_startup:
        repository = ModelRepository(settings.model_repository_root)
        models_settings = await repository.list()

    return settings, models_settings


def install_configured_event_loop(settings: Settings):
    if settings.event_loop == "auto" or settings.event_loop == "uvloop":
        try:
            import uvloop
        except ImportError as e:
            if settings.event_loop == "uvloop":
                raise e
            # else keep the standard asyncio loop as a fallback
        else:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    policy = (
        "uvloop"
        if type(asyncio.get_event_loop_policy()).__module__.startswith("uvloop")
        else "asyncio"
    )

    logger.info(f"Using asyncio event-loop policy: {policy}")


def _path_exists(folder: Union[str, None], file: str) -> bool:
    if folder is None:
        return False

    file_path = os.path.join(folder, file)
    return os.path.isfile(file_path)
