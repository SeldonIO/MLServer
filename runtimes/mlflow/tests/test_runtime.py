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
