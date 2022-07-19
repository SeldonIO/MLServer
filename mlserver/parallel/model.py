from ..model import MLModel
from ..types import MetadataModelResponse, InferenceRequest, InferenceResponse
from ..errors import InferenceError
from ..utils import generate_uuid

from .messages import ModelRequestMessage, ModelResponseMessage
from .dispatcher import Dispatcher


class ParallelModel(MLModel):
    def __init__(self, model: MLModel, dispatcher: Dispatcher):
        super().__init__(model.settings)
        self._model = model
        self._dispatcher = dispatcher

    async def metadata(self) -> MetadataModelResponse:
        pass

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        internal_id = generate_uuid()
        request_message = ModelRequestMessage(
            id=internal_id,
            model_name=self.name,
            model_version=self.version,
            inference_request=payload,
        )
        response_message = await self._dispatcher.dispatch(request_message)

        if response_message.inference_response is None:
            raise InferenceError(
                "Inference request with internal ID "
                f"{internal_id} returned no value"
            )

        return response_message.inference_response
