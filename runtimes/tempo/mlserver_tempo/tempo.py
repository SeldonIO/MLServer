from tempo.serve.pipeline import Pipeline

from mlserver import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri
from mlserver.types import InferenceRequest, InferenceResponse


class TempoModel(MLModel):
    async def load(self) -> bool:
        pipeline_uri = await get_model_uri(self._settings)

        self._pipeline = Pipeline.load(pipeline_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        payload = self._check_request(payload)

        payload_dict = payload.dict()
        prediction = self._pipeline.request(payload_dict)

        return InferenceResponse(**prediction)

    def _check_request(self, payload: InferenceRequest) -> InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "TempoModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        return payload
