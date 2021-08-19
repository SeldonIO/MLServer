from mlserver_alibi_detect.runtime import AlibiDetectRuntime
from mlserver_alibi_detect.errors import InvalidAlibiDetector
from mlserver.utils import get_model_uri
from alibi_detect.utils.saving import load_detector
from importlib import import_module
from typing import Any
import pickle

ALIBI_DETECT_DRIFT_MODULE = "alibi_detect.cd"


class AlibiDriftDetectRuntime(AlibiDetectRuntime):
    """
    Implementation of the MLModel interface to load and serve Alibi drift models.
    """

    async def load(self) -> bool:

        model_uri = await get_model_uri(self._settings)

        if not bool(self.alibi_detect_settings.init_detector):
            self._model = load_detector(model_uri)
        else:
            detector_data = pickle.load(open(model_uri, "rb"))
            try:
                detector_type = self.alibi_detect_settings.detector_type

                detect_module = import_module(ALIBI_DETECT_DRIFT_MODULE)
                drift_detector = getattr(detect_module, detector_type)
            except Exception as e:
                raise InvalidAlibiDetector(detector_type, self._settings.name, e)

            parameters = self.alibi_detect_settings.init_parameters

            self._model = drift_detector(**detector_data, **parameters)

        self.ready = True
        return self.ready

    async def predict_fn(self, input_data: Any, predictParameters: dict) -> dict:
        parameters = self.alibi_detect_settings.predict_parameters
        return self._model.predict(input_data, **{**parameters, **predictParameters})
