from abc import ABC
from typing import Any, Type

from alibi.api.interfaces import Explainer

from mlserver import ModelSettings
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

        # if we are here we are sure that settings.parameters is set,
        # just helping mypy
        assert settings.parameters is not None
        extra = settings.parameters.extra
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
            self._model = await self._load_from_uri(self._inference_model)

        self.ready = True
        return self.ready

    async def _get_inference_model(self) -> Any:
        raise NotImplementedError
