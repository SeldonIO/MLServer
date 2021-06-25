from mlserver import types, MLModel
from mlserver.handlers.custom import custom_handler


class SumModel(MLModel):
    @custom_handler(rest_path="/my-custom-endpoint")
    def my_payload(self, payload: list) -> int:
        return sum(payload)

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = types.ResponseOutput(
            name="total", shape=[1], datatype="FP32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, outputs=[output])
