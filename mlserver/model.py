from .types import InferenceRequest, InferenceResponse


class Model:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def ready(self) -> bool:
        """
        By default, consider the model ready.
        """
        return True

    def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise NotImplementedError("predict() method not implemented")
