from .types import InferenceRequest, InferenceResponse, MetadataModelResponse
from .settings import ModelSettings


class MLModel:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def __init__(self, settings: ModelSettings):
        self._settings = settings
        self.ready = False

    @property
    def name(self) -> str:
        return self._settings.name

    @property
    def version(self) -> str:
        return self._settings.version

    @property
    def metadata(self) -> MetadataModelResponse:
        return MetadataModelResponse(
            name=self.name,
            versions=self._settings.versions,
            platform=self._settings.platform,
            inputs=self._settings.inputs,
        )

    def load(self) -> bool:
        self.ready = True

    def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise NotImplementedError("predict() method not implemented")
