from typing import List, Type, Union, Any

import numpy as np
from alibi.api.interfaces import Explanation, Explainer
from alibi.saving import load_explainer
from pydantic import BaseSettings

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain.common import AlibiExplainSettings, remote_predict
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class AlibiExplainBlackBoxRuntime(AlibiExplainRuntimeBase):
    """
    Runtime for black box explainer runtime, i.e. explainer that would just need access to infer feature from the
    underlying model (no gradients etc.)
    """

    def __init__(self, settings: ModelSettings, explainer_class: Type[Explainer]):
        explainer_settings = AlibiExplainSettings(**settings.parameters.extra)
        self._explainer_class = explainer_class
        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        # TODO: use init explainer field instead
        if self.settings.parameters.uri is None or self.settings.parameters.uri == ".":
            init_parameters = self.alibi_explain_settings.init_parameters
            init_parameters["predictor"] = self._infer_impl
            self._model = self._explainer_class(**init_parameters)  # type: ignore
        else:
            # load the model from disk
            self._model = load_explainer(self.settings.parameters.uri, predictor=self._infer_impl)

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any, settings: BaseSettings) -> Explanation:
        explain_parameters = settings.explain_parameters
        return self._model.explain(
            input_data,
            **explain_parameters
        )

    def _infer_impl(self, input_data: Union[np.ndarray, List]) -> np.ndarray:
        # TODO: >
        # subclasses would probably have to implement this
        # for now we only support v2 protocol
        # maybe also get the model metadata and confirm / reshape types?
        # should mlflow codec do that?
        np_codec = NumpyCodec()

        # TODO: get it from codec? which explainer sends a list?
        if isinstance(input_data, list):
            input_data = np.array(input_data)

        # TODO: fixme as the reshape is required for mnist models
        num_samples = input_data.shape[0]
        input_data = input_data.reshape((num_samples, 1, -1))

        v2_request = InferenceRequest(
            parameters=Parameters(content_type=NumpyCodec.ContentType),
            inputs=[
                RequestInput(
                    name="predict",
                    shape=input_data.shape,
                    data=input_data.tolist(),  # we convert list above to np!
                    datatype="FP32",  # TODO: fixme as it will not work for anything!
                )
            ],
        )

        # TODO add some exception handling here
        v2_response = remote_predict(
            v2_payload=v2_request,
            predictor_url=self.alibi_explain_settings.infer_uri)

        return np_codec.decode(v2_response.outputs[0])  # type: ignore # TODO: fix mypy and first output
