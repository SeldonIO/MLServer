import os
from typing import List, Optional
from mlserver.repository.repository import (
    ModelRepository,
    DEFAULT_MODEL_SETTINGS_FILENAME,
)
from mlserver.settings import ModelSettings
from mlserver.errors import ModelNotFound

from ..fixtures import SumModel, ErrorModel, SimpleModel


class DummyModelRepository(ModelRepository):
    def __init__(self, extra_params: Optional[dict] = None) -> None:

        self._model_settings = []

        if extra_params:
            model_settings_files = extra_params["files"]
            for model_settings_file in model_settings_files:
                model_settings_path = model_settings_file
                model_settings = ModelSettings.parse_file(model_settings_path)
                self._model_settings.append(model_settings)

    async def list(self) -> List[ModelSettings]:
        return self._model_settings

    async def find(self, name: str) -> List[ModelSettings]:
        all_settings = await self.list()
        result = []
        for model_settings in all_settings:
            if model_settings.name == name:
                result.append(model_settings)

        if len(result) == 0:
            raise ModelNotFound(name)

        return result
