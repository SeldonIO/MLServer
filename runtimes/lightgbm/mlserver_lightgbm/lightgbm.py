import lightgbm as lgb

from mlserver import types
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri, to_ndarray


WELLKNOWN_MODEL_FILENAMES = ["model.bst"]


class LightGBMModel(MLModel):
    """
    Implementationof the MLModel interface to load and serve `lightgbm` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        self._model = lgb.Booster(model_file=model_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)

        # _check_request will convert the data to `np.ndarray`
        model_input = payload.inputs[0]
        data = model_input.parameters["data"]  # type: ignore
        prediction = self._model.predict(data)

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
                "LightGBM only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        # Convert to `numpy.ndarray` and store in parameters
        try:
            model_input = payload.inputs[0]
            array_data = to_ndarray(model_input)

            model_input.parameters = {"data": array_data}  # type: ignore
        except Exception as e:
            # There are a few things that can go wrong here, e.g. less than 2-D
            # in the array), or input data not compatible with a numpy array
            raise InferenceError("Invalid input to LightGBM") from e

        return payload
