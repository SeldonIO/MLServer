import numpy as np

from mlflow.pyfunc import PyFuncModel

from mlserver.codecs import PandasCodec, NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput

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


async def test_predict_pytorch(runtime_pytorch: MLflowRuntime):
    # The model used here is the MNIST pytorch example in mlflow:
    # https://github.com/mlflow/mlflow/tree/master/examples/pytorch/MNIST
    # input is a 28*28 image
    data = np.random.randn(1, 28*28).astype(np.float32)
    inference_request = InferenceRequest(
        parameters=Parameters(content_type=PandasCodec.ContentType),
        inputs=[
            RequestInput(
                name=f"predict{idx}",
                shape=[1, 1],
                data=[i],
                datatype="FP32",
            ) for idx, i in enumerate(data.flat)],
    )
    response = await runtime_pytorch.predict(inference_request)

    outputs = response.outputs
    assert len(outputs) == 1
    assert outputs[0].name == DefaultOutputName



