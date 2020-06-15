from .types import InferenceRequest, InferenceResponse


class MLModel:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.ready = False

    def load(self):
        self.ready = True

    def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise NotImplementedError("predict() method not implemented")
