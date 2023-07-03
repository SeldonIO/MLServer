import json
from typing import Tuple

import numpy as np
from pytest_cases import fixture, parametrize_with_cases
from alibi.api.interfaces import Explainer
from numpy.testing import assert_array_almost_equal

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest
from mlserver.settings import ModelSettings
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.common import convert_from_bytes

EXPLANATION_KEY = {  # Explanation key to compare for each explainer type
    'tree_shap': 'shap_values',
    'tree_partial_dependence': 'pd_values',
}


@fixture
@parametrize_with_cases("model_settings, explainer, request, explain_kwargs")
async def test_case(model_settings: ModelSettings, explainer: Explainer,
                    request: InferenceRequest, explain_kwargs: dict) \
        -> Tuple[AlibiExplainRuntime, Explainer, InferenceRequest, dict]:
    """
    Fixture that unpacks the test case into a tuple of the explainer runtime, explainer object, inference request
    and explain kwargs. The pytest-cases doesn't work too well yet with AsyncIO, therefore we need to treat the
    fixture as an Awaitable and await it in the tests (See https://github.com/smarie/python-pytest-cases/issues/286).
    The `explainer`, `request` and `explain_kwargs` are simply passed through.
    """
    runtime = AlibiExplainRuntime(model_settings)
    runtime.ready = await runtime.load()
    return runtime, explainer, request, explain_kwargs


async def test_end_2_end(test_case):
    """
    End-to-end test for the Alibi Explain runtime. This test is parametrized by a separate test case for each of the
    supported explainer types.
    """
    explainer_runtime, explainer, payload, explain_kwargs = await test_case

    # Send an inference request to the explainer runtime
    runtime_result = await explainer_runtime.predict(payload)
    decoded_runtime_results = json.loads(
        convert_from_bytes(runtime_result.outputs[0], ty=str)
    )

    # Perform inference on the local explainer
    input_data_np = NumpyCodec.decode_input(payload.inputs[0])
    explanation = explainer.explain(input_data_np, **explain_kwargs)

    # Compare the results from the runtime and the local explainer
    explainer_type = explainer_runtime.settings.parameters.extra['explainer_type']
    assert_array_almost_equal(
        np.array(decoded_runtime_results["data"][EXPLANATION_KEY[explainer_type]]),
        explanation.data[EXPLANATION_KEY[explainer_type]],
    )
