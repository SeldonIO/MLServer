from typing import Callable
from enum import Enum

from ..handlers.custom import get_custom_handlers, register_custom_handler
from ..model import MLModel
from ..types import MetadataModelResponse, InferenceRequest, InferenceResponse
from ..errors import InferenceError
from ..utils import generate_uuid

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
        self._add_custom_handlers()

    def _add_custom_handlers(self):
        custom_handlers = get_custom_handlers(self._model)
        for handler, method in custom_handlers:
            parallelised = self._parallelise(method)
            register_custom_handler(handler, parallelised)
            setattr(self, method.__name__, parallelised)

    def _parallelise(self, method: Callable):
        async def _inner(*args, **kwargs):
            return await self._send(method.__name__, *args, **kwargs)

        return _inner

    async def metadata(self) -> MetadataModelResponse:
        # TODO: Cache metadata
        return await self._send(ModelMethods.Metadata.value)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        return await self._send(ModelMethods.Predict.value, payload)

    async def _send(self, method_name: str, *args, **kwargs):
        internal_id = generate_uuid()
        req_message = ModelRequestMessage(
            id=internal_id,
            model_name=self.name,
            model_version=self.version,
            method_name=method_name,
            method_args=args,
            method_kwargs=kwargs
        )

        response_message = await self._dispatcher.dispatch(req_message)
        return response_message.response

