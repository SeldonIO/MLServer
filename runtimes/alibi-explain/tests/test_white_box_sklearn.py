import json
from typing import Tuple, Union
import os
import joblib

import numpy as np
from pytest_cases import fixture, parametrize_with_cases, parametrize
from alibi.api.interfaces import Explainer
from numpy.testing import assert_array_almost_equal
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor, XGBModel
from lightgbm import LGBMClassifier, LGBMRegressor, LGBMModel

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest
from mlserver.settings import ModelSettings
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.explainers.sklearn_api_runtime import SKLearnRuntime
from mlserver_alibi_explain.common import convert_from_bytes

EXPLANATION_KEY = {  # Explanation key to compare for each explainer type
    "tree_shap": "shap_values",
    "tree_partial_dependence": "pd_values",
}


@fixture
@parametrize_with_cases(
    "model_settings, explainer, request, explain_kwargs", import_fixtures=True
)
async def test_case(
    model_settings: ModelSettings,
    explainer: Explainer,
    request: InferenceRequest,
    explain_kwargs: dict,
) -> Tuple[AlibiExplainRuntime, Explainer, InferenceRequest, dict]:
    """
    Fixture that unpacks the test case into a tuple of the explainer runtime, explainer
    object, inference request and explain kwargs. The pytest-cases doesn't work too well
    yet with AsyncIO, therefore we need to treat the fixture as an Awaitable and await
    it in the tests (See https://github.com/smarie/python-pytest-cases/issues/286).
    The `explainer`, `request` and `explain_kwargs` are simply passed through.
    """
    runtime = AlibiExplainRuntime(model_settings)
    runtime.ready = await runtime.load()  # type: ignore[attr-defined]
    return runtime, explainer, request, explain_kwargs


async def test_explain(test_case):
    """
    Test the explain method of the Alibi Explain runtime. This test is parametrized by a
    separate test case for each of supported explainer types. The explanations from the
    runtime and the equivalent local explainer are compared.
    """
    explainer_runtime, explainer, payload, explain_kwargs = test_case

    # Send an inference request to the explainer runtime
    runtime_result = await explainer_runtime.predict(payload)
    decoded_runtime_results = json.loads(
        convert_from_bytes(runtime_result.outputs[0], ty=str)
    )

    # Perform inference on the local explainer
    input_data_np = NumpyCodec.decode_input(payload.inputs[0])
    explanation = explainer.explain(input_data_np, **explain_kwargs)

    # Compare the results from the runtime and the local explainer
    explainer_type = explainer_runtime.settings.parameters.extra["explainer_type"]
    assert_array_almost_equal(
        np.array(decoded_runtime_results["data"][EXPLANATION_KEY[explainer_type]]),
        explanation.data[EXPLANATION_KEY[explainer_type]],
    )


@fixture
def mocked_sklearn_runtime(mocker):
    """
    Fixture that returns a mocked Alibi Explain runtime, so that we can test the
    _get_inference_model method without needing to init and serialise an explainer.
    """
    mocked_rt = mocker.Mock()
    mocked_rt.name = "foo"
    return mocked_rt


@fixture
@parametrize(
    "model_class",
    [
        RandomForestClassifier,
        RandomForestRegressor,
        XGBClassifier,
        XGBRegressor,
    ],
)
def white_box_model(
    income_data, model_class, tmp_path
) -> Tuple[Union[BaseEstimator, XGBModel, LGBMModel], str, np.ndarray]:
    """
    Fixture that returns a white box model (and it's uri) for testing.
    """
    # Get training data
    train_size, test_size = 100, 5
    X_train, y_train = income_data["X"][:train_size], income_data["Y"][:train_size]
    # If model is a regressor, convert data to regression problem
    regression = "Regressor" in model_class.__name__
    if regression:
        y_train = X_train[:, 8]  # use the capital gain as the target
        X_train = np.delete(X_train, 8, axis=1)

    # Init and fit model
    model = model_class()
    model.fit(X_train, y_train)

    # Save model
    if "sklearn" in model_class.__module__:
        model_uri = os.path.join(tmp_path, "model.joblib")
        joblib.dump(model, model_uri)
    else:
        raise ValueError(f"Unsupported model type: {model_class.__name__}")
    return model, model_uri, X_train[:test_size]


async def test_get_inference_model(mocked_sklearn_runtime, white_box_model):
    """
    Test the _get_inference_model method of the Alibi Explain runtime. The model is
    loaded from a given uri, and the loaded model is compared to the original model
    type.
    """
    model, model_uri, test_data = white_box_model

    # Inject model uri and load the model
    mocked_sklearn_runtime.alibi_explain_settings.infer_uri = model_uri
    loaded_model = await SKLearnRuntime._get_inference_model(mocked_sklearn_runtime)

    # Check the loaded model
    assert isinstance(loaded_model, type(model))
    np.testing.assert_array_equal(
        loaded_model.predict(test_data), model.predict(test_data)
    )
    if hasattr(model, "predict_proba"):
        np.testing.assert_array_equal(
            loaded_model.predict_proba(test_data), model.predict_proba(test_data)
        )
