from typing import Type, Any

import numpy as np
from alibi.api.interfaces import Explanation, Explainer
from alibi.saving import load_explainer
from pydantic import BaseSettings

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters
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

    def _infer_impl(self, input_data: np.ndarray) -> np.ndarray:
        # The contract is that alibi-explain would input/output ndarray
        # TODO: for now we only support v2 protocol, do we need more support?
        np_codec = NumpyCodec

        v2_request = InferenceRequest(
            parameters=Parameters(content_type=NumpyCodec.ContentType),
            # TODO: we probably need to tell alibi about the expected types to use or even whether it is a
            # proba or targets etc
            inputs=[np_codec.encode_request_input(name="predict", payload=input_data)],
        )

        # TODO add some exception handling here
        v2_response = remote_predict(
            v2_payload=v2_request,
            predictor_url=self.alibi_explain_settings.infer_uri)

        # TODO: do we care about more than one output?
        return np_codec.decode_response_output(v2_response.outputs[0])
