import uuid

from ..settings import Settings
from ..registry import MultiModelRegistry
from ..types import (
    MetadataModelResponse,
    MetadataServerResponse,
    InferenceRequest,
    InferenceResponse,
)
from ..middleware import inference_middlewares


class DataPlane:
    """
    Internal implementation of handlers, used by both the gRPC and REST
    servers.
    """

    def __init__(self, settings: Settings, model_registry: MultiModelRegistry):
        self._settings = settings
        self._model_registry = model_registry

    async def live(self) -> bool:
        return True

    async def ready(self) -> bool:
        models = await self._model_registry.get_models()
        return all([model.ready for model in models])

    async def model_ready(self, name: str, version: str = None) -> bool:
        model = await self._model_registry.get_model(name, version)
        return model.ready

    async def metadata(self) -> MetadataServerResponse:
        return MetadataServerResponse(
            name=self._settings.server_name,
            version=self._settings.server_version,
            extensions=self._settings.extensions,
        )

    async def model_metadata(
        self, name: str, version: str = None
    ) -> MetadataModelResponse:
        model = await self._model_registry.get_model(name, version)
        # TODO: Make await optional for sync methods
        return await model.metadata()

    async def infer(
        self, payload: InferenceRequest, name: str, version: str = None
    ) -> InferenceResponse:
        if payload.id is None:
            payload.id = str(uuid.uuid4())

        model = await self._model_registry.get_model(name, version)

        # Run middlewares
        inference_middlewares(payload, model._settings)

        # TODO: Make await optional for sync methods
        prediction = await model.predict(payload)

        # Ensure ID matches
        prediction.id = payload.id

        return prediction
