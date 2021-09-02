import numpy as np

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from mlserver.handlers.custom import custom_handler


class SumModel(MLModel):
    @custom_handler(rest_path="/my-custom-endpoint")
    def my_payload(self, payload: list) -> int:
        return sum(payload)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded = self.decode(payload.inputs[0])
        total = decoded.sum(axis=1)

        output = ResponseOutput(
            name="total", shape=[len(total), 1], datatype="FP32", data=total
        )
        return InferenceResponse(id=payload.id, model_name=self.name, outputs=[output])
