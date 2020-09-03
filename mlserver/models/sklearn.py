from typing import List

from .. import types
from ..model import MLModel
from ..errors import InferenceError

_SKLEARN_PRESENT = False

try:
    import joblib

    _SKLEARN_PRESENT = True
except ImportError:
    # TODO: Log warning message
    pass

PREDICT_OUTPUT = "predict"
PREDICT_PROBA_OUTPUT = "predict_proba"
VALID_OUTPUTS = [PREDICT_OUTPUT, PREDICT_PROBA_OUTPUT]


class SKLearnModel(MLModel):
    """
    Implementation of the MLModel interface to load and serve `scikit-learn`
    models persisted with `joblib`.
    """

    async def load(self) -> bool:
        # TODO: Log info message
        model_uri = self._settings.parameters.uri
        self._model = joblib.load(model_uri)

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        payload = self._check_request(payload)

        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=self._predict_outputs(payload),
        )

    def _check_request(self, payload: types.InferenceRequest) -> types.InferenceRequest:
        if len(payload.inputs) != 1:
            raise InferenceError(
                "SKLearnModel only supports a single input tensor "
                f"({len(payload.inputs)} were received)"
            )

        if len(payload.outputs) == 0:
            # By default, only return the result of `predict()`
            payload.outputs.append(types.RequestOutput(name=PREDICT_OUTPUT))
        else:
            for request_output in payload.outputs:
                if request_output.name not in VALID_OUTPUTS:
                    raise InferenceError(
                        f"SKLearnModel only supports '{PREDICT_OUTPUT}' and "
                        f"'{PREDICT_PROBA_OUTPUT}' as outputs "
                        f"({request_output.name} was received)"
                    )

        return payload

    def _predict_outputs(
        self, payload: types.InferenceRequest
    ) -> List[types.ResponseOutput]:
        # TODO: Does this need to be a numpy array?
        model_input = payload.inputs[0]

        outputs = []
        for request_output in payload.outputs:
            predict_fn = getattr(self._model, request_output.name)
            y = predict_fn(model_input.data)

            # TODO: Set datatype (cast from numpy?)
            outputs.append(
                types.ResponseOutput(
                    name=request_output.name,
                    shape=y.shape,
                    datatype="FP32",
                    data=y.tolist(),
                )
            )

        return outputs
