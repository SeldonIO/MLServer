from textwrap import dedent

from ..model import MLModel

try:
    import joblib
except ImportError:
    # TODO: Log warning message


class SKLearnModel(MLModel):
    """
    Implementation of the MLModel interface to load and serve `scikit-learn`
    models persisted with `joblib`.
    """

    def load(self) -> bool:
        # TODO: Log info message
        model_uri = self._settings.parameters.model_uri
        self._model = joblib.load(model_uri)

        self.ready = True
        return self.ready

    def predict(self, payload: types.InferenceRequest): -> types.InferenceResponse
        pass
