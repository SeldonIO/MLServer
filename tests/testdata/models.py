from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse


class SumModel(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode(payload.inputs[0])
        total = decoded.sum(axis=1, keepdims=True)

        output = NumpyCodec().encode(name="total", payload=total)
        return InferenceResponse(id=payload.id, model_name=self.name, outputs=[output])
