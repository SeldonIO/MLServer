from mlserver_alibi_detect.runtime import AlibiDetectRuntime
from mlserver_alibi_detect.errors import InvalidAlibiDetector
from mlserver.utils import get_model_uri
from alibi_detect.utils.saving import load_detector
import pickle


class AlibiDriftDetectRuntime(AlibiDetectRuntime):
    """
    Implementation of the MLModel interface to load and serve Alibi drift models.
    """

    async def load(self) -> bool:

        model_uri = await get_model_uri(self._settings)

        if not self.alibi_detect_settings.init_detector:
            try:
                self._model = load_detector(model_uri)
            except (
                ValueError,
                FileNotFoundError,
                EOFError,
                pickle.UnpicklingError,
            ) as e:
                raise InvalidAlibiDetector(self._settings.name) from e
        else:
            try:
                detector_data = pickle.load(open(model_uri, "rb"))
                drift_detector = self.alibi_detect_settings.detector_type
            except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
                raise InvalidAlibiDetector(self._settings.name) from e

            parameters = self.alibi_detect_settings.init_parameters

            self._model = drift_detector(**detector_data, **parameters)

        self.ready = True
        return self.ready
