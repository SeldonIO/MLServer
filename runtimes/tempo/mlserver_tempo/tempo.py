from tempo.serve.pipeline import Pipeline

from mlserver import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri, to_ndarray
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput


class TempoModel(MLModel):
    async def load(self) -> bool:
        pipeline_uri = await get_model_uri(self._settings)

        self._pipeline = Pipeline.load(pipeline_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        payload = self._check_request(payload)

        prediction = await self._pipeline.request(payload)

        # TODO: Set datatype (cast from numpy?)
        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[
                ResponseOutput(
                    name="predict",
                    shape=prediction.shape,
                    datatype="FP32",
                    data=prediction.tolist(),
                )
            ],
        )

    def _check_request(self, payload: InferenceRequest) -> InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "TempoModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        return payload
