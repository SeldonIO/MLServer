from typing import Any, Type, Dict

from alibi.api.interfaces import Explanation, Explainer
from alibi.saving import load_explainer

from mlserver import ModelSettings
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class AlibiExplainWhiteBoxRuntime(AlibiExplainRuntimeBase):
    """
    White box alibi explain requires access to the full inference model
    to compute gradients etc. usually in the same
    domain as the explainer itself. e.g. `IntegratedGradients`
    """

    def __init__(self, settings: ModelSettings, explainer_class: Type[Explainer]):
        self._inference_model = None
        self._explainer_class = explainer_class

        explainer_settings = AlibiExplainSettings(**settings.parameters.extra)
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
            self._model = load_explainer(
                self.settings.parameters.uri, predictor=self._inference_model
            )

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any, explain_parameters: Dict) -> Explanation:
        raise NotImplementedError

    async def _get_inference_model(self) -> Any:
        raise NotImplementedError
