from typing import Tuple

from alibi.api.interfaces import Explainer

from mlserver.types import InferenceRequest
from mlserver.settings import ModelSettings
from .helpers.utils import build_test_case


def case_tree_shap_uri(sk_income_model, income_data, tmp_path) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreeShap explainer with a sklearn classifier. Load from uri.
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


def case_tree_partial_dependence_uri(sk_income_model, income_data, tmp_path) \
        -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreePartialDependence explainer with a sklearn classifier. Load from uri.
    """
    # Set kwargs
    init_kwargs = {
        'predictor': sk_income_model,
        'feature_names': income_data['feature_names'],
        'categorical_names': income_data['category_map'],
        'target_names': income_data['target_names'],
    }
    explain_kwargs = {'features': [0, 2]}

    return build_test_case('tree_partial_dependence', init_kwargs, explain_kwargs, fit=False,
                           save_dir=tmp_path, payload=income_data['X'][:1])


## TODO - Skip PartialDependenceVariance for now since it cannot be saved.
##  See https://github.com/SeldonIO/alibi/issues/938
#def case_tree_partial_dependence_variance_uri(sk_income_model, income_data, tmp_path) \
#        -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
#    """
#    TreePartialDependence explainer with a sklearn classifier. Load from uri.
#    """
#    # Set kwargs
#    init_kwargs = {
#        'predictor': sk_income_model,
#        'feature_names': income_data['feature_names'],
#        'categorical_names': income_data['category_map'],
#        'target_names': income_data['target_names'],
#    }
#    explain_kwargs = {'features': [0, 2]}
#
#    return build_test_case('tree_partial_dependence_variance', init_kwargs, explain_kwargs, fit=False,
#                           save_dir=tmp_path, payload=income_data['X'][:1])
