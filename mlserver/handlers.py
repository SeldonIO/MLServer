from .registry import ModelRegistry
from .types import InferenceRequest, InferenceResponse


class DataPlane:
    """
    Internal implementation of handlers, used by both the gRPC and REST
    servers.
    """

    def __init__(self, model_registry: ModelRegistry):
        self._model_registry = model_registry

    def live(self) -> bool:
        return True

    def ready(self) -> bool:
        models = self._model_registry.get_models()
        return all([model.ready() for model in models])

    def model_ready(self, model_name: str) -> bool:
        # TODO: Handle model version
        model = self._model_registry.get_model(model_name)
        # TODO: Handle model not found errors
        return model.ready()

    def metadata(self):
        pass

    def model_metadata(self, model_name: str):
        # TODO: Handle model version
        pass

    def infer(self, model_name: str, payload: InferenceRequest) -> InferenceResponse:
        # TODO: Handle model version
        model = self._model_registry.get_model(model_name)
        # TODO: Handle model not found errors
        # TODO: Handle prediction errors
        return model.predict(payload)
