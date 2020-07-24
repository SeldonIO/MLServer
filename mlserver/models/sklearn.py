from .. import types
from ..model import MLModel
from ..errors import InferenceError

_SKLEARN_PRESENT = False

try:
    import joblib

    _SKLEARN_PRESENT = True
except ImportError:
    # TODO: Log warning message
    pass


class SKLearnModel(MLModel):
    """
    Implementation of the MLModel interface to load and serve `scikit-learn`
    models persisted with `joblib`.
    """

    def load(self) -> bool:
        # TODO: Log info message
        model_uri = self._settings.parameters.uri
        self._model = joblib.load(model_uri)

        self.ready = True
        return self.ready

    def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "SKLearnModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        # TODO: Does this need to be a numpy array?
        model_input = payload.inputs[0]
        y = self._model.predict(model_input.data)

        # TODO: Set datatype (cast from numpy?)
        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name="predict", shape=y.shape, datatype="FP32", data=y
                )
            ],
        )
