from .settings import Settings
from .repository import ModelRepository
from .types import (
    MetadataModelResponse,
    MetadataServerResponse,
    InferenceRequest,
    InferenceResponse,
)


class DataPlane:
    """
    Internal implementation of handlers, used by both the gRPC and REST
    servers.
    """

    def __init__(self, settings: Settings, model_repository: ModelRepository):
        self._settings = settings
        self._model_repository = model_repository

    def live(self) -> bool:
        return True

    def ready(self) -> bool:
        models = self._model_repository.get_models()
        return all([model.ready for model in models])

    def model_ready(self, name: str, version: str) -> bool:
        model = self._model_repository.get_model(name, version)
        return model.ready

    def metadata(self) -> MetadataServerResponse:
        return MetadataServerResponse(
            name=self._settings.server_name,
            version=self._settings.server_version,
            extensions=self._settings.extensions,
        )

    def model_metadata(self, name: str, version: str) -> MetadataModelResponse:
        model = self._model_repository.get_model(name, version)
        return model.metadata()

    def infer(
        self, name: str, version: str, payload: InferenceRequest
    ) -> InferenceResponse:
        model = self._model_repository.get_model(name, version)
        return model.predict(payload)
