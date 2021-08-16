import numpy as np
import pickle
from mlserver import types
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec
from alibi_detect.cd import TabularDrift

categories_per_feature = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    11: None,
}
p_val = 0.05


def getArgsfromParams(parameters: types.Parameters) -> dict:
    return {"drift_type": parameters.__getattribute__("drift_type")}


class AlibiDetector(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(self._settings)
        ref_data = pickle.load(open(model_uri, "rb"))

        self._model = TabularDrift(ref_data, p_val, categories_per_feature)
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)
        model_input = payload.inputs[0]
        default_codec = NumpyCodec()
        input_data = self.decode(model_input, default_codec=default_codec)

        y = self._model.predict(input_data, **getArgsfromParams(payload.parameters))
        output_data = np.array(y["data"]["is_drift"])

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=[default_codec.encode(name="detect", payload=output_data)],
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "AlibiDetector only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )
        return payload
