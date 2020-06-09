from .types import InferenceRequest, InferenceResponse


class Model:
    def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise NotImplementedError("predict() method not implemented")
