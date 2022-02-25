from mlserver import types
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
import numpy as np
from typing import Optional, Any


class AlibiDetectRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):
        super().__init__(settings)

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        y = await self.predict_fn(
            input_data, payload.parameters.__getattribute__("predict_kwargs")
        )

        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode(name=key, payload=np.array([y["data"][key]]))
            )
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=outputs,
        )

    async def predict_fn(self, input_data: Any, parameters: Optional[dict]) -> dict:
        return self._model.predict(input_data, **parameters)  # type: ignore
