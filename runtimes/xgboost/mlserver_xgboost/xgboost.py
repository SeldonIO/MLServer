import xgboost as xgb

from typing import List
from xgboost.sklearn import XGBModel

from mlserver.errors import InferenceError
from mlserver.model import MLModel
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyRequestCodec, NumpyCodec
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestOutput,
    ResponseOutput,
)

PREDICT_OUTPUT = "predict"
PREDICT_PROBA_OUTPUT = "predict_proba"
VALID_OUTPUTS = [PREDICT_OUTPUT, PREDICT_PROBA_OUTPUT]

WELLKNOWN_MODEL_FILENAMES = ["model.bst", "model.json"]


def _load_sklearn_interface(model_uri: str) -> XGBModel:
    try:
        regressor = xgb.XGBRegressor()
        regressor.load_model(model_uri)
        return regressor
    except TypeError:
        # If there was an error, it's likely due to the model being a
        # classifier
        classifier = xgb.XGBClassifier()
        classifier.load_model(model_uri)
        return classifier


class XGBoostModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `xgboost` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        self._model = _load_sklearn_interface(model_uri)

        self.ready = True
        return self.ready

    def _check_request(self, payload: InferenceRequest) -> InferenceRequest:
        if not payload.outputs:
            # By default, only return the result of `predict()`
            payload.outputs = [RequestOutput(name=PREDICT_OUTPUT)]
        else:
            for request_output in payload.outputs:
                if request_output.name not in VALID_OUTPUTS:
                    raise InferenceError(
                        f"XGBoostModel only supports '{PREDICT_OUTPUT}' and "
                        f"'{PREDICT_PROBA_OUTPUT}' as outputs "
                        f"({request_output.name} was received)"
                    )

        # Regression models do not support `predict_proba`
        if PREDICT_PROBA_OUTPUT in [o.name for o in payload.outputs]:
            if isinstance(self._model, xgb.XGBRegressor):
                raise InferenceError(
                    f"XGBRegressor models do not support '{PREDICT_PROBA_OUTPUT}"
                )

        return payload

    def _get_model_outputs(self, payload: InferenceRequest) -> List[ResponseOutput]:
        decoded_request = self.decode_request(payload, default_codec=NumpyRequestCodec)

        outputs = []
        for request_output in payload.outputs:  # type: ignore
            predict_fn = getattr(self._model, request_output.name)
            y = predict_fn(decoded_request)

            output = self.encode(y, request_output, default_codec=NumpyCodec)
            outputs.append(output)

        return outputs

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        payload = self._check_request(payload)
        outputs = self._get_model_outputs(payload)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=outputs,
        )
