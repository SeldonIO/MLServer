from typing import Optional, Any

from alibi.api.interfaces import Explanation
from alibi.explainers import AnchorImage
from pydantic import BaseSettings
from tensorflow.python.keras.applications.inception_v3 import InceptionV3

from mlserver import ModelSettings
from mlserver_alibi_explain.common import ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS, ExplainerEnum
from mlserver_alibi_explain.runtime import AlibiExplainRuntimeBase


class AlibiExplainSettings(BaseSettings):
    """
    Parameters that apply only to alibi explain models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_EXPLAIN_SETTINGS

    infer_uri: Optional[str]
    init_explainer: bool
    explainer_type: ExplainerEnum
    call_parameters: Optional[dict]
    init_parameters: Optional[dict]


class AnchorImageWrapper(AlibiExplainRuntimeBase):
    def __init__(self, settings: ModelSettings):
        explainer_settings = AlibiExplainSettings(**settings.parameters.extra)
        # TODO: validate the settings are ok with this specific explainer
        super().__init__(settings, explainer_settings)

    async def load(self) -> bool:
        self._model = AnchorImage(
            predictor=self._infer_impl,
            image_shape=self.alibi_explain_settings.init_parameters["image_shape"],
            segmentation_fn=self.alibi_explain_settings.init_parameters["segmentation_fn"],
            segmentation_kwargs=self.alibi_explain_settings.init_parameters["segmentation_kwargs"],
            images_background=None)

        self.ready = True
        return self.ready

    def _explain_impl(self, input_data: Any) -> Explanation:
        return self._model.explain(input_data, threshold=.95, p_sample=.5, tau=0.25)


