import pytest
import xgboost as xgb

from mlserver.models.xgboost import XGBoostModel

from .helpers import skipif_xgboost_missing


@skipif_xgboost_missing
def test_xgboost_load(xgboost_model: XGBoostModel):
    assert xgboost_model.ready
    assert type(xgboost_model._model) == xgb.Booster
