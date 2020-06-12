from mlserver.model import Model
from mlserver import types


class SumModel(Model):
    def __init__(self, name: str = "sum-model"):
        self.name = name

    def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = types.ResponseOutput(
            name="total", shape=[1], datatype="INT32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, id="1", outputs=[output])
