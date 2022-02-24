from mlserver import types
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
import numpy as np
from typing import Optional, Any
from pydantic import BaseSettings, PyObject

ENV_PREFIX_ALIBI_DETECT_SETTINGS = "MLSERVER_MODEL_ALIBI_DETECT_"


class AlibiDetectSettings(BaseSettings):
    """
    Parameters that apply only to alibi detect models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_DETECT_SETTINGS

    init_detector: bool = False
    detector_type: PyObject = ""  # type: ignore
    init_parameters: Optional[dict] = {}
    predict_parameters: Optional[dict] = {}


class AlibiDetectRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):
        if settings.parameters is None:
            self.alibi_detect_settings = AlibiDetectSettings()
        else:
            extra = settings.parameters.extra
            self.alibi_detect_settings = AlibiDetectSettings(**extra)  # type: ignore
        super().__init__(settings)

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        y = await self.predict_fn(input_data)

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

    async def predict_fn(self, input_data: Any) -> dict:
        parameters = self.alibi_detect_settings.predict_parameters
        return self._model.predict(input_data, **parameters)  # type: ignore
