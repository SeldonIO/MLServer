import os
import glob

from typing import List

from .settings import ModelParameters, ModelSettings
from .errors import ModelNotFound
from .logging import logger

DEFAULT_MODEL_SETTINGS_FILENAME = "model-settings.json"


class ModelRepository:
    """
    Model repository, responsible of the discovery of models which can be
    loaded onto the model registry.
    """

    def __init__(self, root: str = None):
        self._root = root

    async def list(self) -> List[ModelSettings]:
        all_model_settings = []

        # TODO: Use an async alternative for filesys ops
        if self._root:
            pattern = os.path.join(self._root, "**", DEFAULT_MODEL_SETTINGS_FILENAME)
            matches = glob.glob(pattern, recursive=True)

            for model_settings_path in matches:
                model_settings = self._load_model_settings(model_settings_path)
                all_model_settings.append(model_settings)

        # If there were no matches, try to load model from environment
        if not all_model_settings:
            # return default
            model_settings = ModelSettings()
            model_settings.parameters = ModelParameters()
            all_model_settings.append(model_settings)

        return all_model_settings

    def _load_model_settings(self, model_settings_path: str) -> ModelSettings:
        model_settings = ModelSettings.parse_file(model_settings_path)
        model_settings._source = model_settings_path

        # If name not present, default to folder name
        model_settings_folder = os.path.dirname(model_settings_path)
        folder_name = os.path.basename(model_settings_folder)
        if model_settings.name:
            if not self._folder_matches(folder_name, model_settings):
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

    def _folder_matches(self, folder_name: str, model_settings: ModelSettings) -> bool:
        if model_settings.name == folder_name:
            return True

        # To be compatible with Triton, check whether the folder name matches
        # with the model's version
        if model_settings.parameters and model_settings.parameters.version:
            model_version = model_settings.parameters.version
            if model_version == folder_name:
                return True

        return False

    async def find(self, name: str) -> List[ModelSettings]:
        all_settings = await self.list()
        selected = []
        for model_settings in all_settings:
            # TODO: Implement other version policies (e.g. "Last N")
            if model_settings.name == name:
                selected.append(model_settings)

        if len(selected) == 0:
            raise ModelNotFound(name)

        return selected
