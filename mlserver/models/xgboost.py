import os

from .. import types
from ..model import MLModel
from ..errors import InferenceError

_XGBOOST_PRESENT = False

try:
    import xgboost as xgb
    import numpy as np

    _XGBOOST_PRESENT = True
except ImportError:
    # TODO: Log warning message
    pass


WELLKNOWN_MODEL_FILENAMES = ["model.bst"]


class XGBoostModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `xgboost` models.
    """

    async def load(self) -> bool:
        # TODO: Log info message
        model_uri = await self._get_model_uri()
        self._model = xgb.Booster(model_file=model_uri)

        self.ready = True
        return self.ready

    async def _get_model_uri(self) -> str:
        model_uri = self._settings.parameters.uri

        # If model_uri is a folder, search for a well-known model filename
        if os.path.isdir(model_uri):
            for fname in WELLKNOWN_MODEL_FILENAMES:
                model_path = os.path.join(model_uri, fname)
                if os.path.isfile(model_path):
                    return model_path

        return model_uri

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)

        # _check_request will convert the data to `xgboost.DMatrix`
        model_input = payload.inputs[0]
        dmatrix_data = model_input.parameters["dmatrix_data"]
        prediction = self._model.predict(dmatrix_data)

        # TODO: Set datatype (cast from numpy?)
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name="predict",
                    shape=prediction.shape,
                    datatype="FP32",
                    data=prediction.tolist(),
                )
            ],
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "XGBoostModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        # Convert to `xgboost.DMatrix` and store in parameters
        # TODO: Move this out to "types conversion" pipeline, once it's there.
        try:
            model_input = payload.inputs[0]
            array_data = np.array(model_input.data)
            dmatrix_data = xgb.DMatrix(array_data)

            model_input.parameters = {"dmatrix_data": dmatrix_data}
        except Exception as e:
            # There are a few things that can go wrong here, e.g. less than 2-D
            # in the array), or input data not compatible with a numpy array
            raise InferenceError("Invalid input to XGBoostModel") from e

        return payload
