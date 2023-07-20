import asyncio

from typing import AsyncIterator

from mlserver import types, MLModel
from mlserver.codecs import NumpyRequestCodec


class SumModel(MLModel):
    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = types.ResponseOutput(
            name="total", shape=[1, 1], datatype="FP32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, id="1", outputs=[output])


class StreamModel(MLModel):
    response_chunks = 5

    async def predict_stream(
        self, payload: types.InferenceRequest
    ) -> AsyncIterator[types.InferenceResponse]:
        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)

        for idx in range(self.response_chunks):
            await asyncio.sleep(0.5)
            yield NumpyRequestCodec.encode_response(
                model_name=self.name, payload=decoded + idx, model_version=self.version
            )
