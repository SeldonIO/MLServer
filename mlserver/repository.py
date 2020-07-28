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

    def index(self):
        pass

    def load(self, model: MLModel):
        model.load()

        # TODO: Raise warning if model already exists
        self._models[model.name][model.version] = model

        # TODO: Improve logic to choose default version of the model
        self._default_models[model.name] = model
        self._flat_models.append(model)

    def unload(self):
        pass

    def get_model(self, name: str, version: str = None) -> MLModel:
        if name not in self._models:
            raise ModelNotFound(name, version)

        if version is not None:
            models = self._models[name]
            if version not in models:
                raise ModelNotFound(name, version)

        return self._default_models[name]

    def get_models(self) -> List[MLModel]:
        return self._flat_models
