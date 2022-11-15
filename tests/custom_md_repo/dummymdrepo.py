import os
from typing import List
from mlserver.repository.repository import (
    ModelRepository,
    DEFAULT_MODEL_SETTINGS_FILENAME,
)
from mlserver.settings import ModelSettings
from mlserver.errors import ModelNotFound

from ..fixtures import SumModel, ErrorModel, SimpleModel

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


class DummyModelRepository(ModelRepository):
    def __init__(self, extra_params: dict) -> None:
        model_settings_path = os.path.join(
            TESTDATA_PATH, DEFAULT_MODEL_SETTINGS_FILENAME
        )
        model_settings = ModelSettings.parse_file(model_settings_path)

        self._model_settings = [model_settings]

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
