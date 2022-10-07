from mlserver import types, MLModel
from mlserver.logging import logger


class SumModel(MLModel):
    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        logger.debug("printin things")
        logger.info("printin more things (as info)")
        logger.warning("now this is a warning!")
        total = 0
        for inp in payload.inputs:
            total += sum(inp.data)

        output = types.ResponseOutput(
            name="total", shape=[1], datatype="FP32", data=[total]
        )
        return types.InferenceResponse(model_name=self.name, id="1", outputs=[output])
