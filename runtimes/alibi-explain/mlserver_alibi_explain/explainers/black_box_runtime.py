from typing import Type, Any, Dict, Optional, List, Union

import numpy as np
from alibi.api.interfaces import Explanation, Explainer
from alibi.saving import load_explainer

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec
from mlserver.errors import ModelParametersMissing, InvalidModelURI
from mlserver.settings import ModelParameters
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

        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        # TODO: use init explainer field instead?
        if self.alibi_explain_settings.init_parameters is not None:
            init_parameters = self.alibi_explain_settings.init_parameters
            init_parameters["predictor"] = self._infer_impl
            self._model = self._explainer_class(**init_parameters)  # type: ignore
        else:
            # load the model from disk
            model_parameters: Optional[ModelParameters] = self.settings.parameters
            if model_parameters is None:
                raise ModelParametersMissing(self.name)

            uri = model_parameters.uri

            if uri is None:
                raise InvalidModelURI(self.name)

            self._model = load_explainer(uri, predictor=self._infer_impl)

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

        # TODO add some exception handling here
        infer_uri = self.alibi_explain_settings.infer_uri
        assert infer_uri is not None, "infer_uri has to be set"
        v2_response = remote_predict(v2_payload=v2_request, predictor_url=infer_uri)

        # TODO: do we care about more than one output?
        return NumpyCodec.decode_response_output(v2_response.outputs[0])
