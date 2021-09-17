from typing import Optional, Any

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
        # TODO: wire up the settings
        segmentation_fn = "slic"
        kwargs = {"n_segments": 15, "compactness": 20, "sigma": .5}

        # TODO: image_shape, what can we do with this? can it be loaded from model metadata?
        image_shape = (299, 299, 3)  # this is just for testing, remove

        self._model = AnchorImage(
            self.predict_fn,
            image_shape,
            segmentation_fn=segmentation_fn,
            segmentation_kwargs=kwargs,
            images_background=None)

        self.ready = True
        return self.ready

    async def predict_fn(self, input_data: Any) -> dict:
        model = InceptionV3(weights='imagenet')
        return model.predict(input_data)


