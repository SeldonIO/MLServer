from typing import Any

import tensorflow as tf
from alibi.api.interfaces import Explanation
from pydantic import BaseSettings

from mlserver_alibi_explain.explainers.white_box_runtime import AlibiExplainWhiteBoxRuntime


class IntegratedGradientsWrapper(AlibiExplainWhiteBoxRuntime):
    def _explain_impl(self, input_data: Any, settings: BaseSettings) -> Explanation:
        # TODO: how are we going to deal with that?
        predictions = self._inference_model(input_data).numpy().argmax(axis=1)
        explain_parameters = settings.explain_parameters
        return self._model.explain(
            input_data,
            target=predictions,
            **explain_parameters
        )

    async def _get_inference_model(self) -> Any:
        inference_model_path = self.alibi_explain_settings.infer_uri
        return tf.keras.models.load_model(inference_model_path)


