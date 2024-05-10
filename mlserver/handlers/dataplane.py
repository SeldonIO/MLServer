from prometheus_client import (
    Counter,
    Summary,
)
from typing import Optional

from ..errors import ModelNotReady
from ..context import model_context
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
from ..cache import ResponseCache, LocalCache


class DataPlane:
    """
    Internal implementation of handlers, used by both the gRPC and REST
    servers.
    """

    def __init__(self, settings: Settings, model_registry: MultiModelRegistry):
        self._settings = settings
        self._model_registry = model_registry
        self._response_cache = None
        if settings.cache_enabled:
            self._response_cache = self._create_response_cache()
        self._inference_middleware = InferenceMiddlewares(
            CloudEventsMiddleware(settings)
        )

        # TODO: Update to standardised set of labels
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
        with model_context(model.settings):
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

        if self._response_cache is not None:
            cache_key = payload.model_dump_json()

        with infer_duration, infer_errors:
            if payload.id is None:
                payload.id = generate_uuid()

            model = await self._model_registry.get_model(name, version)
            if not model.ready:
                raise ModelNotReady(name, version)

            self._inference_middleware.request_middleware(payload, model.settings)

            # TODO: Make await optional for sync methods
            with model_context(model.settings):
                if (
                    self._response_cache is not None
                    and model.settings.cache_enabled is not False
                ):
                    cache_value = await self._response_cache.lookup(cache_key)
                    if cache_value != "":
                        prediction = InferenceResponse.parse_raw(cache_value)
                    else:
                        prediction = await model.predict(payload)
                        # ignore cache insertion error if any
                        await self._response_cache.insert(
                            cache_key, prediction.model_dump_json()
                        )
                else:
                    prediction = await model.predict(payload)

            # Ensure ID matches
            prediction.id = payload.id

            self._inference_middleware.response_middleware(prediction, model.settings)

            self._ModelInferRequestSuccess.labels(model=name, version=version).inc()

            return prediction

    def _create_response_cache(self) -> ResponseCache:
        return LocalCache(size=self._settings.cache_size)

    def _get_response_cache(self) -> Optional[ResponseCache]:
        return self._response_cache
