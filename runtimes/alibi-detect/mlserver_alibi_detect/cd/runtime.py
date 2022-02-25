from mlserver_alibi_detect.runtime import AlibiDetectRuntime
from mlserver_alibi_detect.errors import InvalidAlibiDetectorConfiguration
from mlserver.utils import get_model_uri
from alibi_detect.utils.saving import load_detector


class AlibiDriftDetectRuntime(AlibiDetectRuntime):
    """
    Implementation of the MLModel interface to load and serve Alibi drift models.
    """

    async def load(self) -> bool:

        model_uri = await get_model_uri(self._settings)
        try:
            self._model = load_detector(model_uri)
        except (ValueError, FileNotFoundError, EOFError) as e:
            raise InvalidAlibiDetectorConfiguration(self._settings.name) from e

        self.ready = True
        return self.ready
