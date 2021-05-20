import lightgbm as lgb

from mlserver import types
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec


WELLKNOWN_MODEL_FILENAMES = ["model.bst"]


class LightGBMModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `lightgbm` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        self._model = lgb.Booster(model_file=model_uri)

        self._codec = NumpyCodec()

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
            outputs=[self._codec.encode(name="predict", payload=prediction)],
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "LightGBM only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        return payload
