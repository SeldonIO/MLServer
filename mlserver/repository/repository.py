import os
import glob

from pydantic.error_wrappers import ValidationError
from typing import Optional, List

from ..settings import ModelParameters, ModelSettings
from ..errors import ModelNotFound
from ..logging import logger

from .load import load_model_settings

DEFAULT_MODEL_SETTINGS_FILENAME = "model-settings.json"


class ModelRepository:
    """
    Model repository, responsible of the discovery of models which can be
    loaded onto the model registry.
    """

    def __init__(self, root: Optional[str] = None):
        self._root = root

    async def list(self) -> List[ModelSettings]:
        all_model_settings = []

        # TODO: Use an async alternative for filesys ops
        if self._root:
            abs_root = os.path.abspath(self._root)
            pattern = os.path.join(abs_root, "**", DEFAULT_MODEL_SETTINGS_FILENAME)
            matches = glob.glob(pattern, recursive=True)

            for model_settings_path in matches:
                try:
                    model_settings = load_model_settings(model_settings_path)
                    all_model_settings.append(model_settings)
                except Exception:
                    logger.exception(
                        f"Failed load model settings at {model_settings_path}."
                    )

        # If there were no matches, try to load model from environment
        if not all_model_settings:
            logger.debug(f"No models were found in repository at {self._root}.")
            try:
                # return default
                model_settings = ModelSettings()
                model_settings.parameters = ModelParameters()
                all_model_settings.append(model_settings)
            except ValidationError:
                logger.debug("No default model found in environment settings.")

        return all_model_settings

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
