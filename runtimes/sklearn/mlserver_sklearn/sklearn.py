import joblib

from typing import List, Tuple

import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from mlserver import types
from mlserver.codecs.base import find_input_codec, find_request_codec
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.types import ResponseOutput, RequestOutput
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec, NumpyRequestCodec, PandasCodec

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

        model_responses = self._get_model_outputs(payload)

        if (len(model_responses) == 1 and isinstance(model_responses[0][1], DataFrame)):
            print("Trying to encode data frame")
            df: DataFrame = model_responses[0][1]
            return PandasCodec.encode(model_name=self.name,
                                      model_version=self.version,
                                      payload=df)

        print("Not encoding dataframe")
        return types.InferenceResponse(
                model_name=self.name,
                model_version=self.version,
                outputs=self._encode_outputs(model_responses),
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

    def _get_model_outputs(self, payload: types.InferenceRequest) -> List[Tuple[RequestOutput, object]]:
        decoded_request = self.decode_request(payload, default_codec=NumpyRequestCodec)

        outputs = []
        for request_output in payload.outputs:  # type: ignore
            predict_fn = getattr(self._model, request_output.name)
            y = predict_fn(decoded_request)
            outputs.append((request_output, y))

        return outputs

    def _encode_outputs(self, outputs: List[Tuple[RequestOutput, object]]) -> List[types.ResponseOutput]:
        response_outputs = []

        all_output_names = [o[0].name for o in outputs]

        for output, response in outputs:
            if isinstance(response, pd.DataFrame):
                raise InferenceError(f"{output.name} is of type DataFrame and {all_output_names} were"
                                     f" requested. Cannot encode multiple DataFrames in one response."
                                     f" Please request only a single DataFrame output.")

            # TODO: accommodate more things like Strings
            response_output = NumpyCodec.encode(name=output.name, payload=response)
            response_outputs.append(response_output)

        return response_outputs
