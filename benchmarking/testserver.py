"""
Starts an inference server.
"""
from mlserver import types, MLServer, MLModel, Settings


class SumModel(MLModel):
    def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = types.ResponseOutput(
            name="total", shape=[1], datatype="FP32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, id="1", outputs=[output])


def main():
    settings = Settings(debug=False)
    sum_model = SumModel(name="sum-model", version="v1.2.3")

    server = MLServer(settings, models=[sum_model])
    server.start()


if __name__ == "__main__":
    main()
