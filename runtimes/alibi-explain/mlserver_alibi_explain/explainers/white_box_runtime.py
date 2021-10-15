from abc import ABC
from typing import Any, Type, Optional

from alibi.api.interfaces import Explainer
from alibi.saving import load_explainer

from mlserver import ModelSettings
from mlserver.errors import ModelParametersMissing, InvalidModelURI
from mlserver.settings import ModelParameters
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class AlibiExplainWhiteBoxRuntime(ABC, AlibiExplainRuntimeBase):
    """
    White box alibi explain requires access to the full inference model
    to compute gradients etc. usually in the same
    domain as the explainer itself. e.g. `IntegratedGradients`
    """

    def __init__(self, settings: ModelSettings, explainer_class: Type[Explainer]):
        self._inference_model = None
        self._explainer_class = explainer_class

        extra = settings.parameters.extra  # type: ignore
        explainer_settings = AlibiExplainSettings(**extra)  # type: ignore

        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        self._inference_model = await self._get_inference_model()

        if self.alibi_explain_settings.init_parameters is not None:
            init_parameters = self.alibi_explain_settings.init_parameters
            # white box explainers requires access to the inference model
            init_parameters["model"] = self._inference_model
            self._model = self._explainer_class(**init_parameters)  # type: ignore
        else:
            # load the model from disk
            # full model is passed as `predictor`
            # load the model from disk
            model_parameters: Optional[ModelParameters] = self.settings.parameters
            if model_parameters is None:
                raise ModelParametersMissing(self.name)

            uri = model_parameters.uri

            if uri is None:
                raise InvalidModelURI(self.name)

            self._model = load_explainer(uri, predictor=self._inference_model)

        self.ready = True
        return self.ready

    async def _get_inference_model(self) -> Any:
        raise NotImplementedError
