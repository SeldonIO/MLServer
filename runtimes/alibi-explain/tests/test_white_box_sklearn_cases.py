from typing import Tuple

import pytest
from alibi.api.interfaces import Explainer

from mlserver.types import InferenceRequest
from mlserver.settings import ModelSettings
from .helpers.utils import build_test_case


def case_tree_shap(sk_income_model, income_data, tmp_path) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreeShap explainer with a sklearn classifier. Test load from uri only (as requires fitting).
    """
    # Set kwargs
    init_kwargs = {
        'predictor': sk_income_model,
        'feature_names': income_data['feature_names'],
        'model_output': 'raw',
        'task': 'classification',
    }
    explain_kwargs = {}

    return build_test_case('tree_shap', init_kwargs, explain_kwargs, fit='no-data',  # fit w/o data i.e. path-dep. algo
                           save_dir=tmp_path, payload=income_data['X'][:1])


@pytest.mark.parametrize('save', [True, False])
def case_tree_partial_dependence(sk_income_model, income_data, tmp_path, save) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreePartialDependence explainer with a sklearn classifier. Test Load from uri and init w/ params.
    """
    # Set kwargs
    init_kwargs = {
        'predictor': sk_income_model,
        'feature_names': income_data['feature_names'],
        'categorical_names': income_data['category_map'],
        'target_names': income_data['target_names'],
    }
    explain_kwargs = {'features': [0, 2]}

    save_dir = tmp_path if save else None
    return build_test_case('tree_partial_dependence', init_kwargs, explain_kwargs, fit=False,
                           save_dir=save_dir, payload=income_data['X'][:1])
