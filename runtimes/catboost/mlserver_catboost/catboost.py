import os

import numpy as np

from catboost import CatBoostClassifier

from mlserver import types
from mlserver.model import MLModel
from mlserver.errors import InferenceError
from mlserver.utils import get_model_uri
from mlserver.codecs import NumpyCodec, NumpyRequestCodec


WELLKNOWN_MODEL_FILENAMES = ["model.cbm", "model.bin"]


class CatboostModel(MLModel):
    """
    Implementation of the MLModel interface to load and serve `catboost` models.
    """

    async def load(self) -> bool:
        model_uri = await get_model_uri(
            self._settings, wellknown_filenames=WELLKNOWN_MODEL_FILENAMES
        )

        self._model = CatBoostClassifier()
        self._model.load_model(model_uri)
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        output_names = [output.name for output in payload.outputs or []]
        if not output_names:
            predict_fn = None
            if self.settings.parameters and self.settings.parameters.extra:
                predict_fn = self.settings.parameters.extra.get("predict_fn")
            if not predict_fn:
                predict_fn = (
                    "predict_proba"
                    if os.getenv("PREDICT_PROBA", "false").lower() == "true"
                    else "predict"
                )
            output_names = [predict_fn]

        for name in output_names:
            if name not in ("predict", "predict_proba"):
                raise InferenceError(
                    f"CatboostModel only supports 'predict' and 'predict_proba' "
                    f"as outputs ({name} was received)"
                )

        decoded = self.decode_request(payload, default_codec=NumpyRequestCodec)
        outputs = []
        for name in output_names:
            prediction = getattr(self._model, name)(decoded)
            if name == "predict_proba":
                prediction = np.atleast_2d(prediction)
            outputs.append(NumpyCodec.encode(name=name, payload=prediction))
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=outputs,
        )
