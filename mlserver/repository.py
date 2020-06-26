from typing import List

from .model import MLModel
from .errors import ModelNotFound


class ModelRepository:
    """
    Model repository interface, inspired in NVIDIA Triton's `model-repository`
    extension.
    """

    def __init__(self):
        self._models = {}

    def index(self):
        pass

    def load(self, model: MLModel):
        model.load()

        # TODO: Raise warning if model already exists
        model_key = self._get_key(model.name, model.version)
        self._models[model_key] = model

    def unload(self):
        pass

    def get_model(self, name: str, version: str) -> MLModel:
        model_key = self._get_key(name, version)
        if model_key not in self._models:
            raise ModelNotFound(name, version)

        return self._models[model_key]

    def _get_key(self, name: str, version: str) -> str:
        return f"{name}-{version}"

    def get_models(self) -> List[MLModel]:
        return self._models.values()
