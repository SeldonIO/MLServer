from mlserver import types
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.utils import get_model_uri
from alibi_detect.utils.saving import load_detector
from mlserver.errors import MLServerError, InferenceError
from pydantic.error_wrappers import ValidationError
import numpy as np


class AlibiDetectRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):
        super().__init__(settings)

    async def load(self) -> bool:

        model_uri = await get_model_uri(self._settings)
        try:
            self._model = load_detector(model_uri)
        except (
            ValueError,
            FileNotFoundError,
            EOFError,
            NotImplementedError,
            ValidationError,
        ) as e:
            raise MLServerError(
                f"Invalid configuration for model {self._settings.name}: {e}"
            ) from e

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        predict_kwargs = {}
        if payload.parameters is not None:
            predict_kwargs = payload.parameters.predict_kwargs

        try:
            y = self._model.predict(input_data, **predict_kwargs)
        except (ValueError, IndexError) as e:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {e}"
            ) from e

        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode(name=key, payload=np.array([y["data"][key]]))
            )
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=outputs,
        )
