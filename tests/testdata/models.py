import asyncio

from mlserver import MLModel

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, InferenceResponse


class SumModel(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode(payload.inputs[0])
        total = decoded.sum(axis=1, keepdims=True)

        output = NumpyCodec().encode(name="total", payload=total)
        return InferenceResponse(id=payload.id, model_name=self.name, outputs=[output])


class SlowModel(MLModel):
    async def load(self) -> bool:
        await asyncio.sleep(10)
        self.ready = True
        return self.ready

    async def infer(self, payload: InferenceRequest) -> InferenceResponse:
        await asyncio.sleep(10)
        return InferenceResponse(id=payload.id, model_name=self.name, outputs=[])
