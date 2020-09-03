from typing import List
from collections import defaultdict

from .model import MLModel
from .errors import ModelNotFound


class ModelRepository:
    """
    Model repository interface, inspired in NVIDIA Triton's `model-repository`
    extension.
    """

    def __init__(self):
        self._models = defaultdict(dict)
        self._default_models = {}
        self._flat_models = []

    async def index(self):
        pass

    async def load(self, model: MLModel):
        await model.load()

        # TODO: Raise warning if model already exists
        self._models[model.name][model.version] = model

        # TODO: Improve logic to choose default version of the model
        self._default_models[model.name] = model
        self._flat_models.append(model)

    async def unload(self):
        pass

    async def get_model(self, name: str, version: str = None) -> MLModel:
        if name not in self._models:
            raise ModelNotFound(name, version)

        # Check that `version` is neither None nor an empty string
        if version:
            models = self._models[name]
            if version not in models:
                raise ModelNotFound(name, version)

        return self._default_models[name]

    async def get_models(self) -> List[MLModel]:
        return self._flat_models
