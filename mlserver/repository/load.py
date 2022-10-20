import os

from ..settings import ModelParameters, ModelSettings
from ..logging import logger


def load_model_settings(model_settings_path: str) -> ModelSettings:
    model_settings = ModelSettings.parse_file(model_settings_path)

    # If name not present, default to folder name
    model_settings_folder = os.path.dirname(model_settings_path)
    folder_name = os.path.basename(model_settings_folder)
    if model_settings.name:
        if not _folder_matches(folder_name, model_settings):
            # Raise warning if name is different than folder's name
            logger.warning(
                f"Model name '{model_settings.name}' is different than "
                f"model's folder name '{folder_name}'."
            )
    else:
        model_settings.name = folder_name

    if not model_settings.parameters:
        model_settings.parameters = ModelParameters()

    if not model_settings.parameters.uri:
        # If not specified, default to its own folder
        default_model_uri = os.path.dirname(model_settings_path)
        model_settings.parameters.uri = default_model_uri

    return model_settings


def _folder_matches(folder_name: str, model_settings: ModelSettings) -> bool:
    if model_settings.name == folder_name:
        return True

    # To be compatible with Triton, check whether the folder name matches
    # with the model's version
    if model_settings.parameters and model_settings.parameters.version:
        model_version = model_settings.parameters.version
        if model_version == folder_name:
            return True

    return False
