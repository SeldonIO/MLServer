import xgboost as xgb

from xgboost.sklearn import XGBModel

from mlserver.model import MLModel
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyRequestCodec, NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse, RequestOutput


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

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)
        # TODO: Do something similar to SKLearn runtime to support either
        # predict or predict_proba
        prediction = self._model.predict(decoded)

        request_output = RequestOutput(name="predict")
        output = self.encode(
            prediction, request_output=request_output, default_codec=NumpyCodec
        )
        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[output],
        )
