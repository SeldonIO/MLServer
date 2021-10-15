from typing import Any, Dict

import tensorflow as tf
from alibi.api.interfaces import Explanation

from mlserver.errors import InvalidModelURI
from mlserver_alibi_explain.explainers.white_box_runtime import (
    AlibiExplainWhiteBoxRuntime,
)


class IntegratedGradientsWrapper(AlibiExplainWhiteBoxRuntime):
    def _explain_impl(self, input_data: Any, explain_parameters: Dict) -> Explanation:
        # TODO: how are we going to deal with that?
        assert self._inference_model is not None, "Inference model is not set"
        predictions = self._inference_model(input_data).numpy().argmax(axis=1)
        return self._model.explain(input_data, target=predictions, **explain_parameters)

    async def _get_inference_model(self) -> Any:
        inference_model_path = self.alibi_explain_settings.infer_uri
        try:
            model = tf.keras.models.load_model(inference_model_path)
        except IOError:
            raise InvalidModelURI(self.name, inference_model_path)

        return model
