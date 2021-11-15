import joblib

from typing import List

from sklearn.pipeline import Pipeline

from mlserver import types
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec


PREDICT_OUTPUT = "predict"
PREDICT_PROBA_OUTPUT = "predict_proba"
VALID_OUTPUTS = [PREDICT_OUTPUT, PREDICT_PROBA_OUTPUT]

WELLKNOWN_MODEL_FILENAMES = ["model.joblib", "model.pickle", "model.pkl"]


class SKLearnModel(MLModel):
    """
    Implementation of the MLModel interface to load and serve `scikit-learn`
    models persisted with `joblib`.
    """

    async def load(self) -> bool:
        # TODO: Log info message
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )
        self._model = joblib.load(model_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=self._predict_outputs(payload),
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if not payload.outputs:
            # By default, only return the result of `predict()`
            payload.outputs = [types.RequestOutput(name=PREDICT_OUTPUT)]
        else:
            for request_output in payload.outputs:
                if request_output.name not in VALID_OUTPUTS:
                    raise InferenceError(
                        f"SKLearnModel only supports '{PREDICT_OUTPUT}' and "
                        f"'{PREDICT_PROBA_OUTPUT}' as outputs "
                        f"({request_output.name} was received)"
                    )

        # Regression models do not support `predict_proba`
        if PREDICT_PROBA_OUTPUT in [o.name for o in payload.outputs]:
            # Ensure model supports it
            maybe_regressor = self._model
            if isinstance(self._model, Pipeline):
                maybe_regressor = maybe_regressor.steps[-1][-1]

            if not hasattr(maybe_regressor, PREDICT_PROBA_OUTPUT):
                raise InferenceError(
                    f"{type(maybe_regressor)} models do not support "
                    f"'{PREDICT_PROBA_OUTPUT}"
                )

        return payload

    def _predict_outputs(
        self, payload: types.InferenceRequest
    ) -> List[types.ResponseOutput]:
        default_codec = NumpyCodec()
        # TODO: how to set default codec here? Needs to be in the request...?
        decoded_request = self.decode_request(payload)

        # If we decode to an InferenceRequest again,
        # then inputs is probably an array of tensors
        if isinstance(decoded_request, types.InferenceRequest):
            if len(decoded_request.inputs) != 1:
                raise InferenceError(
                    "SKLearnModel only supports a single input tensor "
                    f"({len(payload.inputs)} were received)"
                )
            input_data = decoded_request.inputs[0]
        # Otherwise we decoded to a different structure e.g. a pandas.DataFrame
        else:
            input_data = decoded_request

        outputs = []
        for request_output in payload.outputs:  # type: ignore
            predict_fn = getattr(self._model, request_output.name)
            y = predict_fn(input_data)

            # TODO: Set datatype (cast from numpy?)
            response_output = default_codec.encode(name=request_output.name, payload=y)
            outputs.append(response_output)

        return outputs
