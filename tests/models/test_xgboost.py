import xgboost as xgb

from mlserver.models.xgboost import XGBoostModel
from mlserver.types import InferenceRequest

from .helpers import skipif_xgboost_missing


@skipif_xgboost_missing
def test_xgboost_load(xgboost_model: XGBoostModel):
    assert xgboost_model.ready
    assert type(xgboost_model._model) == xgb.Booster


@skipif_xgboost_missing
def test_xgboost_predict(
    xgboost_model: XGBoostModel, xgboost_inference_request: InferenceRequest
):
    response = xgboost_model.predict(xgboost_inference_request)

    assert len(response.outputs) == 1
    breakpoint()
