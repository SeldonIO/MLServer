from typing import Type, Union, Callable

from .settings import Settings
from .repository import ModelRepository
from .errors import ModelNotFound
from .types import (
    MetadataModelResponse,
    MetadataModelErrorResponse,
    MetadataServerResponse,
    InferenceRequest,
    InferenceResponse,
    InferenceErrorResponse,
)


def _wrap_exception(
    response_class: Union[
        Type[InferenceErrorResponse], Type[MetadataModelErrorResponse]
    ]
):
    def _outer(f):
        def _inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ModelNotFound as err:
                # TODO: Log stacktrace
                return response_class(error=str(err))

        return _inner

    return _outer


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

    @_wrap_exception(MetadataModelErrorResponse)
    def model_metadata(self, name: str, version: str) -> MetadataModelResponse:
        model = self._model_repository.get_model(name, version)
        return model.metadata()

    @_wrap_exception(InferenceErrorResponse)
    def infer(
        self, name: str, version: str, payload: InferenceRequest
    ) -> Union[InferenceResponse, InferenceErrorResponse]:
        model = self._model_repository.get_model(name, version)
        return model.predict(payload)
