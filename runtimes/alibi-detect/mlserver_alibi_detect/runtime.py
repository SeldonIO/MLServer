from mlserver import types
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.utils import get_model_uri
from alibi_detect.utils.saving import load_detector
from mlserver.errors import MLServerError, InferenceError
from pydantic.error_wrappers import ValidationError
from typing import Optional
from pydantic import BaseSettings
import numpy as np

ENV_PREFIX_ALIBI_DETECT_SETTINGS = "MLSERVER_MODEL_ALIBI_DETECT_"

ALIBI_MODULE_NAMES = {"cd": "drift", "od": "outlier", "ad": "adversarial"}


class AlibiDetectSettings(BaseSettings):
    """
    Parameters that apply only to alibi detect models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_DETECT_SETTINGS

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
        if self.alibi_detect_settings.predict_parameters is not None:
            predict_kwargs = self.alibi_detect_settings.predict_parameters

        try:
            y = self._model.predict(np.array(input_data), **predict_kwargs)
        except (ValueError, IndexError) as e:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {e}"
            ) from e

        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode_output(name=key, payload=np.array([y["data"][key]]))
            )
        # Add headers
        y["meta"]["headers"] = {
            "x-seldon-alibi-type": self.get_alibi_type(),
            "x-seldon-alibi-method": self.get_alibi_method(),
        }
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=outputs,
        )

    def get_alibi_method(self) -> str:
        module: str = type(self._model).__module__
        return module.split(".")[-1]

    def get_alibi_type(self) -> str:
        module: str = type(self._model).__module__
        method = module.split(".")[-2]
        if method in ALIBI_MODULE_NAMES:
            return ALIBI_MODULE_NAMES[method]
        else:
            return "unknown"
