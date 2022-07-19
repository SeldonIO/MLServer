from ..model import MLModel
from ..types import MetadataModelResponse, InferenceRequest, InferenceResponse

from .dispatcher import Dispatcher


class ParallelModel(MLModel):
    def __init__(self, model: MLModel, dispatcher: Dispatcher):
        super().__init__(model.settings)
        self._model = model
        self._dispatcher = dispatcher

    async def metadata(self) -> MetadataModelResponse:
        pass

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        return await self._dispatcher.predict(self.settings, payload)
