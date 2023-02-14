from ..settings import Settings
from ..registry import MultiModelRegistry
from ..types import (
    MetadataModelResponse,
    MetadataServerResponse,
    InferenceRequest,
    InferenceResponse,
)
from ..middleware import InferenceMiddlewares
from ..cloudevents import CloudEventsMiddleware
from ..utils import generate_uuid
from prometheus_client import (
    Counter,
    Summary,
)
from typing import Optional


class DataPlane:
    """
    Internal implementation of handlers, used by both the gRPC and REST
    servers.
    """

    def __init__(self, settings: Settings, model_registry: MultiModelRegistry):
        self._settings = settings
        self._model_registry = model_registry

        self._inference_middleware = InferenceMiddlewares(
            CloudEventsMiddleware(settings)
        )

        self._ModelInferRequestSuccess = Counter(
            "model_infer_request_success",
            "Model infer request success count",
            ["model", "version"],
        )
        self._ModelInferRequestFailure = Counter(
            "model_infer_request_failure",
            "Model infer request failure count",
            ["model", "version"],
        )
        self._ModelInferRequestDuration = Summary(
            "model_infer_request_duration",
            "Model infer request duration",
            ["model", "version"],
        )

    async def live(self) -> bool:
        return True

    async def ready(self) -> bool:
        models = await self._model_registry.get_models()
        return all([model.ready for model in models])

    async def model_ready(self, name: str, version: Optional[str] = None) -> bool:
        model = await self._model_registry.get_model(name, version)
        return model.ready

    async def metadata(self) -> MetadataServerResponse:
        return MetadataServerResponse(
            name=self._settings.server_name,
            version=self._settings.server_version,
            extensions=self._settings.extensions,
        )

    async def model_metadata(
        self, name: str, version: Optional[str] = None
    ) -> MetadataModelResponse:
        model = await self._model_registry.get_model(name, version)
        # TODO: Make await optional for sync methods
        return await model.metadata()

    async def infer(
        self,
        payload: InferenceRequest,
        name: str,
        version: Optional[str] = None,
    ) -> InferenceResponse:
        infer_duration = self._ModelInferRequestDuration.labels(
            model=name, version=version
        ).time()
        infer_errors = self._ModelInferRequestFailure.labels(
            model=name, version=version
        ).count_exceptions()

        with infer_duration, infer_errors:
            if payload.id is None:
                payload.id = generate_uuid()

            model = await self._model_registry.get_model(name, version)

            self._inference_middleware.request_middleware(payload, model.settings)

            # TODO: Make await optional for sync methods
            prediction = await model.predict(payload)

            # Ensure ID matches
            prediction.id = payload.id

            self._inference_middleware.response_middleware(prediction, model.settings)

            self._ModelInferRequestSuccess.labels(model=name, version=version).inc()

            return prediction
