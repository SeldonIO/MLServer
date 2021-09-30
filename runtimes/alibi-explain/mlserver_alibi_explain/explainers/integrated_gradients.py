import os
from typing import Any

import tensorflow as tf
from alibi.api.interfaces import Explanation
from alibi.explainers import IntegratedGradients
from pydantic import BaseSettings
from tensorflow.keras.layers import Activation, Conv2D, Dense, Dropout
from tensorflow.keras.layers import Flatten, Input, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

from mlserver import ModelSettings
from mlserver.settings import ModelParameters
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase
from mlserver_mlflow import MLflowRuntime


class IntegratedGradientsWrapper(AlibiExplainRuntimeBase):
    def __init__(self, settings: ModelSettings):
        self._inference_model = None

        explainer_settings = AlibiExplainSettings(**settings.parameters.extra)
        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        self._inference_model = await _get_inference_model(self.alibi_explain_settings.infer_uri)

        if self.settings.parameters.uri is None:
            init_parameters = self.alibi_explain_settings.init_parameters
            self._model = IntegratedGradients(
                model=self._inference_model,
                **init_parameters)
        # TODO: load the model from disk

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any, settings: BaseSettings) -> Explanation:
        # TODO: how are we going to deal with that?
        predictions = self._inference_model(input_data).numpy().argmax(axis=1)
        explain_parameters = settings.explain_parameters
        return self._model.explain(
            input_data,
            target=predictions,
            **explain_parameters
        )


async def _get_inference_model(filepath: str):
    return tf.keras.models.load_model(filepath)

