from typing import Any

from alibi.api.interfaces import Explanation
from alibi.explainers import AnchorImage
from alibi.saving import save_explainer, load_explainer
from pydantic import BaseSettings

from mlserver import ModelSettings
from mlserver_alibi_explain.common import AlibiExplainSettings
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class AnchorImageWrapper(AlibiExplainRuntimeBase):
    def __init__(self, settings: ModelSettings):
        explainer_settings = AlibiExplainSettings(**settings.parameters.extra)
        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        if self.settings.parameters.uri is None:
            self._model = AnchorImage(
                predictor=self._infer_impl,
                image_shape=self.alibi_explain_settings.init_parameters["image_shape"],
                segmentation_fn=self.alibi_explain_settings.init_parameters["segmentation_fn"],
                segmentation_kwargs=self.alibi_explain_settings.init_parameters["segmentation_kwargs"],
                images_background=None)
        else:
            # load the model from disk
            self._model = load_explainer(self.settings.parameters.uri, predictor=self._infer_impl)

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any, settings: BaseSettings) -> Explanation:
        explain_parameters = settings.explain_parameters
        return self._model.explain(
            input_data,
            threshold=explain_parameters["threshold"],
            p_sample=explain_parameters["p_sample"],
            tau=explain_parameters["tau"]
        )


