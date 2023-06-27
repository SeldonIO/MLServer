from typing import Any, Dict

import joblib
import lightgbm as lgb
from xgboost.core import XGBoostError
from lightgbm.basic import LightGBMError
from alibi.api.interfaces import Explanation

from mlserver_xgboost.xgboost import _load_sklearn_interface as load_xgb_model
from mlserver.errors import InvalidModelURI
from mlserver_alibi_explain.explainers.white_box_runtime import (
    AlibiExplainWhiteBoxRuntime,
)


class AlibiExplainSKLearnAPIRuntime(AlibiExplainWhiteBoxRuntime):
    """
    Runtime for white-box explainers that require access to a tree-based model matching the SKLearn API, such as
    a sklearn, XGBoost, or LightGBM model. Example explainers include TreeShap and TreePartialDependence.
    """
    def _explain_impl(self, input_data: Any, explain_parameters: Dict) -> Explanation:
        # TODO: how are we going to deal with that?
        assert self._inference_model is not None, "Inference model is not set"
        return self._model.explain(input_data, **explain_parameters)

    async def _get_inference_model(self) -> Any:
        inference_model_path = self.alibi_explain_settings.infer_uri
        # Attempt to load model in order: XGBoost, LightGBM, sklearn
        # TODO - add support for CatBoost (would require model_type = 'classifier' or 'regressor' in settings)
        try:
            # Try to load as XGBoost model
            model = load_xgb_model(inference_model_path)
        except XGBoostError:
            try:
                # Try to load as LightGBM model
                model = lgb.Booster(model_file=inference_model_path)
            except LightGBMError:
                try:
                    # Try to load as sklearn model
                    model = joblib.load(inference_model_path)
                except (IndexError, KeyError, IOError):
                    raise InvalidModelURI(self.name, inference_model_path)

        return model
