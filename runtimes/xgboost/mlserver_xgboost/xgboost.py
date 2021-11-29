import xgboost as xgb

from mlserver import types
from mlserver.model import MLModel
from mlserver.utils import get_model_uri

from .codecs import DMatrixCodec, DMatrixRequestCodec


WELLKNOWN_MODEL_FILENAMES = ["model.bst", "model.json"]


class XGBoostModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `xgboost` models.
    """

    async def load(self) -> bool:
        # TODO: Log info message
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )
        self._model = xgb.Booster(model_file=model_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        decoded = self.decode_request(payload, default_codec=DMatrixRequestCodec)
        prediction = self._model.predict(decoded)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[DMatrixCodec.encode("predict", prediction)],
        )
