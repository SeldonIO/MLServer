from typing import Any, Callable, Optional
from enum import Enum
from functools import wraps

from ..errors import InferenceError
from ..handlers.custom import get_custom_handlers, register_custom_handler
from ..model import MLModel
from ..types import MetadataModelResponse, InferenceRequest, InferenceResponse

from .messages import ModelRequestMessage
from .dispatcher import Dispatcher


class ModelMethods(Enum):
    Predict = "predict"
    Metadata = "metadata"


class ParallelModel(MLModel):
    def __init__(self, model: MLModel, dispatcher: Dispatcher):
        super().__init__(model.settings)
        self._model = model
        self._dispatcher = dispatcher
        self._metadata: Optional[MetadataModelResponse] = None
        self._add_custom_handlers()

    def _add_custom_handlers(self):
        custom_handlers = get_custom_handlers(self._model)
        for handler, method in custom_handlers:
            parallelised = self._parallelise(method)
            register_custom_handler(handler, parallelised)
            setattr(self, method.__name__, parallelised)

    def _parallelise(self, method: Callable):
        @wraps(method)
        async def _inner(*args, **kwargs):
            return await self._send(method.__name__, *args, **kwargs)

        return _inner

    async def metadata(self) -> MetadataModelResponse:
        # NOTE: We cache metadata to avoid expensive worker calls for static
        # data
        if self._metadata is None:
            metadata_response = await self._send(ModelMethods.Metadata.value)
            if not isinstance(metadata_response, MetadataModelResponse):
                raise InferenceError(f"Model '{self.name}' returned no metadata")

            self._metadata = metadata_response

        return self._metadata

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        inference_response = await self._send(ModelMethods.Predict.value, payload)
        if not isinstance(inference_response, InferenceResponse):
            raise InferenceError(
                f"Model '{self.name}' returned no predictions after inference"
            )

        return inference_response

    async def _send(self, method_name: str, *args, **kwargs) -> Optional[Any]:
        req_message = ModelRequestMessage(
            model_name=self.name,
            model_version=self.version,
            method_name=method_name,
            method_args=args,
            method_kwargs=kwargs,
        )

        response_message = await self._dispatcher.dispatch_request(req_message)
        return response_message.return_value
