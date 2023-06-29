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


EXPLANATION_KEY = {
    'tree_shap': 'shap_values',
    'tree_partial_dependence': 'pd_values',
    'tree_partial_dependence_variance': 'pd_values',
}

@fixture
@parametrize_with_cases("model_settings, explainer, request")
async def explainer_runtime_request(model_settings: ModelSettings, explainer: Explainer, request: InferenceRequest) \
        -> Tuple[AlibiExplainRuntime, Explainer, InferenceRequest]:
    # NOTE: The pytest-cases doesn't work too well yet with AsyncIO, therefore
    # we need to treat the fixture as an Awaitable and await it in the tests.
    # https://github.com/smarie/python-pytest-cases/issues/286
    runtime = AlibiExplainRuntime(model_settings)
    runtime.ready = await runtime.load()
    return runtime, explainer, request


async def test_end_2_end(
        explainer_runtime_request,
):
    explainer_runtime, explainer, payload = await explainer_runtime_request

    # in this test we are getting explanation and making sure that it the same
    # one as returned by alibi
    # directly
    runtime_result = await explainer_runtime.predict(payload)
    decoded_runtime_results = json.loads(
        convert_from_bytes(runtime_result.outputs[0], ty=str)
    )

    # get the data as numpy from the inference request payload
    input_data_np = NumpyCodec.decode_input(payload.inputs[0])
    explanation = explainer.explain(input_data_np)

    explainer_type = explainer_runtime.settings.parameters.extra['explainer_type']
    assert_array_almost_equal(
        np.array(decoded_runtime_results["data"][EXPLANATION_KEY[explainer_type]]),
        explanation.data[EXPLANATION_KEY[explainer_type]],
    )
