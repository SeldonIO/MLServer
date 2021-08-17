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
    import numpy as np
    inference_request = InferenceRequest(
        parameters=Parameters(content_type=PandasCodec.ContentType),
        inputs=[
            RequestInput(
                name=f"predict",
                shape=[1, 28*28],
                data=np.random.randn(1, 28*28).astype(np.float32).tolist(),
                datatype="FP32",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            )],
    )
    response = await runtime_pytorch.predict(inference_request)



