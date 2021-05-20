import numpy as np

from mlflow.pyfunc import PyFuncModel
from mlserver.types import InferenceRequest

from mlserver_mlflow import MLflowRuntime
from mlserver_mlflow.encoding import DefaultOutputName


def test_load(runtime: MLflowRuntime):
    assert runtime.ready

    assert type(runtime._model) == PyFuncModel


async def test_predict(runtime: MLflowRuntime, inference_request: InferenceRequest):
    response = await runtime.predict(inference_request)

    outputs = response.outputs
    assert len(outputs) == 1
    assert outputs[0].name == DefaultOutputName


def test_to_tensor_dict(runtime: MLflowRuntime, inference_request: InferenceRequest):
    tensor_dict = runtime._to_tensor_dict(inference_request)

    expected_dict = {"input-0": np.array([1, 2, 3], dtype=np.int32)}

    assert tensor_dict.keys() == expected_dict.keys()
    for key, val in tensor_dict.items():
        expected_val = expected_dict[key]
        np.testing.assert_array_equal(val, expected_val)
