from typing import Tuple, Dict, Any
import os
import joblib
import pytest

from alibi.api.interfaces import Explainer
from sklearn.ensemble import GradientBoostingClassifier
from alibi.datasets import fetch_adult

from mlserver.types import InferenceRequest
from mlserver.settings import ModelSettings
from .helpers.utils import build_test_case


@pytest.fixture(scope="function")  # must scope as function due to use of tmp_path
def sk_income_model_uri(income_data, tmp_path) -> str:
    X_train, Y_train = income_data["X"], income_data["Y"]

    model = GradientBoostingClassifier(n_estimators=50)
    model.fit(X_train, Y_train)

    model_uri = os.path.join(tmp_path, "sklearn-model.joblib")
    joblib.dump(model, model_uri)

    return model_uri


@pytest.fixture(scope="module")
def income_data() -> dict:
    adult = fetch_adult()
    X = adult.data
    Y = adult.target

    feature_names = adult.feature_names
    category_map = adult.category_map

    # Package into dictionary
    data_dict = {
        "X": X,
        "Y": Y,
        "feature_names": feature_names,
        "category_map": category_map,
        "target_names": adult.target_names,
    }
    return data_dict


def case_tree_shap(
    sk_income_model_uri, income_data, tmp_path
) -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreeShap explainer with a sklearn classifier. Test load from uri only (as requires
    fitting).
    """
    # Set kwargs
    init_kwargs = {
        "feature_names": income_data["feature_names"],
        "model_output": "raw",
        "task": "classification",
    }
    explain_kwargs: Dict[str, Any] = {}

    return build_test_case(
        "tree_shap",
        init_kwargs,
        explain_kwargs,
        fit="no-data",  # fit w/o data i.e. path-dep. algo
        save_dir=tmp_path,
        model_uri=sk_income_model_uri,
        payload=income_data["X"][:1],
    )


@pytest.mark.parametrize("save", [True, False])
def case_tree_partial_dependence(
    sk_income_model_uri, income_data, tmp_path, save
) -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreePartialDependence explainer with a sklearn classifier. Test Load from uri and
    init w/ params.
    """
    # Set kwargs
    init_kwargs = {
        "feature_names": income_data["feature_names"],
        "categorical_names": income_data["category_map"],
        "target_names": income_data["target_names"],
    }
    explain_kwargs = {"features": [0, 2]}

    save_dir = tmp_path if save else None
    return build_test_case(
        "tree_partial_dependence",
        init_kwargs,
        explain_kwargs,
        fit=False,
        save_dir=save_dir,
        model_uri=sk_income_model_uri,
        payload=income_data["X"][:1],
    )


def case_tree_partial_dependence_variance(
    sk_income_model_uri, income_data
) -> Tuple[ModelSettings, Explainer, InferenceRequest, dict]:
    """
    TreePartialDependence explainer with a sklearn classifier. Test Init w/ params.

    # TODO - add load from uri test once https://github.com/SeldonIO/alibi/issues/938
    is fixed.
    """
    # Set kwargs
    init_kwargs = {
        "feature_names": income_data["feature_names"],
        "categorical_names": income_data["category_map"],
        "target_names": income_data["target_names"],
    }
    explain_kwargs = {"features": [0, 2]}

    return build_test_case(
        "tree_partial_dependence",
        init_kwargs,
        explain_kwargs,
        fit=False,
        save_dir=None,
        model_uri=sk_income_model_uri,
        payload=income_data["X"][:1],
    )
