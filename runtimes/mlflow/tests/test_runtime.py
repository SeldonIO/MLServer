import pytest
import numpy as np
import pandas as pd

from typing import Any

from mlserver.codecs import NumpyCodec, PandasCodec
from mlserver.types import (
    InferenceRequest,
    Parameters,
    RequestInput,
    InferenceResponse,
    ResponseOutput,
)
from mlflow.pyfunc import PyFuncModel
from mlflow.models.signature import ModelSignature

from mlserver_mlflow import MLflowRuntime


def test_load(runtime: MLflowRuntime):
    assert runtime.ready

    assert type(runtime._model) == PyFuncModel


async def test_predict(runtime: MLflowRuntime, inference_request: InferenceRequest):
    response = await runtime.predict(inference_request)

    outputs = response.outputs
    assert len(outputs) == 1
    assert outputs[0].name == "output-1"


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
    assert outputs[0].name == "output-1"


@pytest.mark.parametrize(
    "output, expected",
    [
        (
            ["foo"],
            InferenceResponse(
                model_name="mlflow-model",
                outputs=[
                    ResponseOutput(
                        name="output-1",
                        datatype="BYTES",
                        shape=[1, 1],
                        data=[b"foo"],
                        parameters=Parameters(content_type="str"),
                    )
                ],
            ),
        ),
        (
            np.array([[1, 2], [3, 4]], dtype=np.float32),
            InferenceResponse(
                model_name="mlflow-model",
                outputs=[
                    ResponseOutput(
                        name="output-1",
                        datatype="FP32",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                    )
                ],
            ),
        ),
        (
            {"foo": np.array([1, 2, 3]), "bar": np.array([1.2])},
            InferenceResponse(
                model_name="mlflow-model",
                outputs=[
                    ResponseOutput(
                        name="foo", datatype="INT64", shape=[3, 1], data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="bar", datatype="FP64", shape=[1, 1], data=[1.2]
                    ),
                ],
            ),
        ),
        (
            {"foo": np.array([1, 2, 3]), "bar": np.array(["hello", "world"])},
            InferenceResponse(
                model_name="mlflow-model",
                outputs=[
                    ResponseOutput(
                        name="foo", datatype="INT64", shape=[3, 1], data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="BYTES",
                        shape=[2, 1],
                        data=[b"hello", b"world"],
                    ),
                ],
            ),
        ),
        (
            pd.DataFrame({"foo": np.array([1, 2, 3]), "bar": ["A", "B", "C"]}),
            InferenceResponse(
                model_name="mlflow-model",
                outputs=[
                    ResponseOutput(
                        name="foo", datatype="INT64", shape=[3, 1], data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[b"A", b"B", b"C"],
                    ),
                ],
            ),
        ),
    ],
)
async def test_predict_outputs(
    runtime: MLflowRuntime,
    inference_request: InferenceRequest,
    output: Any,
    expected: InferenceResponse,
    mocker,
):
    mocker.patch.object(runtime._model, "predict", return_value=output)
    response = await runtime.predict(inference_request)
    assert response == expected


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
    assert metadata.parameters.content_type == PandasCodec.ContentType
