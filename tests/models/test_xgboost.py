import pytest
import os

from mlserver.models.xgboost import (
    XGBoostModel,
    _XGBOOST_PRESENT,
    WELLKNOWN_MODEL_FILENAMES,
)
from mlserver.settings import ModelSettings
from mlserver.errors import InferenceError
from mlserver.types import InferenceRequest

from .helpers import skipif_xgboost_missing

if _XGBOOST_PRESENT:
    import xgboost as xgb


@skipif_xgboost_missing
def test_xgboost_load(xgboost_model: XGBoostModel):
    assert xgboost_model.ready
    assert type(xgboost_model._model) == xgb.Booster


@skipif_xgboost_missing
@pytest.mark.parametrize("fname", WELLKNOWN_MODEL_FILENAMES)
async def test_xgboost_load_folder(
    fname, xgboost_model_uri: str, xgboost_model_settings: ModelSettings
):
    model_uri = os.path.dirname(xgboost_model_uri)
    model_path = os.path.join(model_uri, fname)
    os.rename(xgboost_model_uri, model_path)

    xgboost_model_settings.parameters.uri = model_uri  # type: ignore

    model = XGBoostModel(xgboost_model_settings)
    await model.load()

    assert model.ready
    assert type(model._model) == xgb.Booster


@skipif_xgboost_missing
async def test_xgboost_predict(
    xgboost_model: XGBoostModel, xgboost_inference_request: InferenceRequest
):
    response = await xgboost_model.predict(xgboost_inference_request)

    assert len(response.outputs) == 1
    assert 0 <= response.outputs[0].data[0] <= 1


@skipif_xgboost_missing
async def test_xgboost_multiple_inputs_error(
    xgboost_model: XGBoostModel, inference_request: InferenceRequest
):
    with pytest.raises(InferenceError):
        await xgboost_model.predict(inference_request)
