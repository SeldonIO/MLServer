from typing import Type, Any, Dict, List, Union

import numpy as np
from alibi.api.interfaces import Explanation, Explainer

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec
from mlserver_alibi_explain.common import (
    AlibiExplainSettings,
    remote_predict,
    to_v2_inference_request,
)
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class AlibiExplainBlackBoxRuntime(AlibiExplainRuntimeBase):
    """
    Runtime for black box explainer runtime, i.e. explainer that would just need access
    to infer feature from the underlying model (no gradients etc.)
    """

    def __init__(self, settings: ModelSettings, explainer_class: Type[Explainer]):
        self._explainer_class = explainer_class

        # if we are here we are sure that settings.parameters is set,
        # just helping mypy
        assert settings.parameters is not None
        extra = settings.parameters.extra
        explainer_settings = AlibiExplainSettings(**extra)  # type: ignore

        self.infer_uri = explainer_settings.infer_uri

        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        # TODO: use init explainer field instead?
        if self.alibi_explain_settings.init_parameters is not None:
            init_parameters = self.alibi_explain_settings.init_parameters
            init_parameters["predictor"] = self._infer_impl
            self._model = self._explainer_class(**init_parameters)  # type: ignore
        else:
            self._model = self._load_from_uri(self._infer_impl)

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any, explain_parameters: Dict) -> Explanation:
        if type(input_data) == list:
            # if we get a list of strings, we can only explain the first elem and there
            # is no way of just sending a plain string in v2, it has to be in a list
            # as the encoding is List[str] with content_type "BYTES"
            input_data = input_data[0]

        return self._model.explain(input_data, **explain_parameters)

    def _infer_impl(self, input_data: Union[np.ndarray, List[str]]) -> np.ndarray:
        # The contract is that alibi-explain would input/output ndarray
        # in the case of AnchorText, we have a list of strings instead though.
        # TODO: for now we only support v2 protocol, do we need more support?

        v2_request = to_v2_inference_request(input_data)

        v2_response = remote_predict(
            v2_payload=v2_request, predictor_url=self.infer_uri
        )

        # TODO: do we care about more than one output?
        return NumpyCodec.decode_response_output(v2_response.outputs[0])
