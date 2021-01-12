import pickle

from mlserver import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri, to_ndarray
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput


class MLOpsModel(MLModel):
    async def load(self) -> bool:
        pipeline_uri = await get_model_uri(self._settings)

        with open(pipeline_uri, "rb") as pipeline_raw:
            self._pipeline = pickle.load(pipeline_raw)

        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # TODO: Call `.pipeline()`

        payload = self._check_request(payload)

        # Convert to ndarray
        model_input = payload.inputs[0]
        input_data = to_ndarray(model_input)

        prediction = self._pipeline.pipeline(input_data)

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
                "MLOpsModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        return payload
