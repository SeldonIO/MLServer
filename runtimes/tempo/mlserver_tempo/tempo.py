from tempo.serve.pipeline import Pipeline

from mlserver import MLModel
from mlserver.utils import get_model_uri
from mlserver.types import InferenceRequest, InferenceResponse


class TempoModel(MLModel):
    async def load(self) -> bool:
        pipeline_uri = await get_model_uri(self._settings)
        self._pipeline = Pipeline.load(pipeline_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        prediction = self._pipeline.request(payload.dict())
        return InferenceResponse(**prediction)
