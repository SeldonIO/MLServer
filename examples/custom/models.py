import numpy as np

from mlserver import types, MLModel


class SumModel(MLModel):
    def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        total = 0
        for inp in payload.inputs:
            data = np.array(inp.data)
            total += data.sum().item()

        output = types.ResponseOutput(
            name="total", shape=[1], datatype="FP32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, id="1", outputs=[output])
