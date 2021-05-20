import xgboost as xgb

from mlserver import types
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri

from .codecs import DMatrixCodec


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
        self._codec = DMatrixCodec()

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)

        model_input = payload.inputs[0]
        decoded = self.decode(model_input, default_codec=self._codec)
        prediction = self._model.predict(decoded)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[self._codec.encode("predict", prediction)],
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "XGBoostModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        return payload
