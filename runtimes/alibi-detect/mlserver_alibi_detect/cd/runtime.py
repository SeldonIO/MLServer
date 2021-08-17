from mlserver_alibi_detect.runtime import AlibiDetectRuntime
from mlserver_alibi_detect.errors import InvalidAlibiDetector
from mlserver.utils import get_model_uri
from alibi_detect.utils.saving import load_detector
from importlib import import_module
import pickle
import numpy as np

AlibiDetectDriftModule = "alibi_detect.cd"


class AlibiDriftDetectRuntime(AlibiDetectRuntime):
    """
    Implementation of the MLModel interface to load and serve Alibi drift models.
    """

    async def load(self) -> bool:

        model_uri = await get_model_uri(self._settings)

        init = bool(self._settings.parameters.extra["init_detector"])
        if not init:
            self._model = load_detector(model_uri)
        else:
            detector_data = pickle.load(open(model_uri, "rb"))
            try:
                detector_type = ""
                if "detector_type" in self._settings.parameters.extra:
                    detector_type = self._settings.parameters.extra["detector_type"]

                detect_module = import_module(AlibiDetectDriftModule)
                drift_detector = getattr(detect_module, detector_type)
            except Exception as e:
                raise InvalidAlibiDetector(detector_type, self._settings.name, e)

            parameters = {}
            if "init_parameters" in self._settings.parameters.extra:
                parameters = self._settings.parameters.extra["init_parameters"]

            self._model = drift_detector(**detector_data, **parameters)

        self.ready = True
        return self.ready

    async def predict_fn(self, input_data: np.array, predictParameters: dict) -> dict:
        parameters = {}
        if "predict_parameters" in self._settings.parameters.extra:
            parameters = self._settings.parameters.extra["predict_parameters"]

        return self._model.predict(input_data, **{**parameters, **predictParameters})
