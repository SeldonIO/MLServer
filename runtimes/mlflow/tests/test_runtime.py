import numpy as np

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlflow.pyfunc import PyFuncModel
from mlflow.models.signature import ModelSignature

from mlserver_mlflow import MLflowRuntime
from mlserver_mlflow.encoding import DefaultOutputName
from mlserver_mlflow.codecs import TensorDictCodec


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
    data = np.random.randn(1, 28 * 28).astype(np.float32)
    inference_request = InferenceRequest(
        parameters=Parameters(content_type=NumpyCodec.ContentType),
        inputs=[
            RequestInput(
                name="predict",
                shape=data.shape,
                data=data.tolist(),
                datatype="FP32",
            )
        ],
    )
    response = await runtime_pytorch.predict(inference_request)

    outputs = response.outputs
    assert len(outputs) == 1
    assert outputs[0].name == DefaultOutputName


async def test_metadata(runtime: MLflowRuntime, model_signature: ModelSignature):
    metadata = await runtime.metadata()

    assert metadata.name == runtime.name
    assert metadata.versions == runtime._settings.versions
    assert metadata.platform == runtime._settings.platform

    assert metadata.inputs is not None
    assert len(model_signature.inputs.inputs) == len(metadata.inputs)

    assert metadata.outputs is not None
    assert len(model_signature.outputs.inputs) == len(metadata.outputs)

    assert metadata.parameters is not None
    assert metadata.parameters.content_type == TensorDictCodec.ContentType
