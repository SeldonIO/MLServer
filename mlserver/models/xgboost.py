from typing import List

from .. import types
from ..model import MLModel
from ..errors import InferenceError

_XGBOOST_PRESENT = False

try:
    import xgboost as xgb

    _XGBOOST_PRESENT = True
except ImportError:
    # TODO: Log warning message
    pass


class XGBoostModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `xgboost` models.
    """

    def load(self) -> bool:
        # TODO: Log info message
        model_uri = self._settings.parameters.uri
        self._model = xgb.Booster(model_file=model_uri)

        self.ready = True
        return self.ready

    def predict(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        pass

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        return payload
