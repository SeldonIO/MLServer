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
        return True

    def metadata(self):
        pass

    def infer(self, model_name: str, payload: InferenceRequest) -> InferenceResponse:
        model = self._model_registry.get_model(model_name)
        # TODO: Handle errors: on prediction and model not found
        return model.predict(payload)
