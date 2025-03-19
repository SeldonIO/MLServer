import pytest
from unittest import mock
import numpy as np
import pandas as pd

from typing import Any
from mlserver.codecs import NumpyCodec, PandasCodec, StringCodec
from mlserver.codecs.pandas import PandasJsonContentType
from mlserver.types import (
    InferenceRequest,
    Parameters,
    RequestInput,
    InferenceResponse,
    ResponseOutput,
)
from mlflow.pyfunc import PyFuncModel
from mlflow.models.signature import ModelSignature
from mlflow.pyfunc.scoring_server import CONTENT_TYPE_CSV, CONTENT_TYPE_JSON

from mlserver_mlflow import MLflowRuntime
from mlserver_mlflow.codecs import TensorDictCodec


def test_load(runtime: MLflowRuntime):
    assert runtime.ready

    assert isinstance(runtime._model, PyFuncModel)


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
                parameters=Parameters(content_type=StringCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="output-1",
                        datatype="BYTES",
                        shape=[1, 1],
                        data=[b"foo"],
                        parameters=Parameters(content_type=StringCodec.ContentType),
                    )
                ],
            ),
        ),
        (
            np.array([[1, 2], [3, 4]], dtype=np.float32),
            InferenceResponse(
                model_name="mlflow-model",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="output-1",
                        datatype="FP32",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    )
                ],
            ),
        ),
        (
            {"foo": np.array([1, 2, 3]), "bar": np.array([1.2])},
            InferenceResponse(
                model_name="mlflow-model",
                parameters=Parameters(content_type=TensorDictCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="INT64",
                        shape=[3, 1],
                        data=[1, 2, 3],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="FP64",
                        shape=[1, 1],
                        data=[1.2],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                ],
            ),
        ),
        (
            {"foo": np.array([1, 2, 3]), "bar": np.array(["hello", "world"])},
            InferenceResponse(
                model_name="mlflow-model",
                parameters=Parameters(content_type=TensorDictCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="INT64",
                        shape=[3, 1],
                        data=[1, 2, 3],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="BYTES",
                        shape=[2, 1],
                        data=[b"hello", b"world"],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                ],
            ),
        ),
        (
            pd.DataFrame({"foo": np.array([1, 2, 3]), "bar": ["A", "B", "C"]}),
            InferenceResponse(
                model_name="mlflow-model",
                parameters=Parameters(content_type=PandasCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="INT64",
                        shape=[3, 1],
                        data=[1, 2, 3],
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[b"A", b"B", b"C"],
                        parameters=Parameters(content_type=StringCodec.ContentType),
                    ),
                ],
            ),
        ),
        (
            pd.DataFrame(
                {
                    "foo": [[1], [1, 2], [1, 2, 3]],
                    "bar": [{"a": 1}, {"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}],
                    "baz": ["a", "b", {"a": 1}],
                    "qux": [
                        {"a": 1, "b": {"c": {"d": 1}}},
                        {"a": 1, "b": {"c": {"d": 1}}, "e": 2},
                        {"a": 1, "b": {"c": {"d": 1}}, "e": 2, "f": 3},
                    ],
                }
            ),
            InferenceResponse(
                model_name="mlflow-model",
                parameters=Parameters(content_type=PandasCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[b"[1]", b"[1,2]", b"[1,2,3]"],
                        parameters=Parameters(content_type=PandasJsonContentType),
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[b'{"a":1}', b'{"a":1,"b":2}', b'{"a":1,"b":2,"c":3}'],
                        parameters=Parameters(content_type=PandasJsonContentType),
                    ),
                    ResponseOutput(
                        name="baz",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[b'"a"', b'"b"', b'{"a":1}'],
                        parameters=Parameters(content_type=PandasJsonContentType),
                    ),
                    ResponseOutput(
                        name="qux",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[
                            b'{"a":1,"b":{"c":{"d":1}}}',
                            b'{"a":1,"b":{"c":{"d":1}},"e":2}',
                            b'{"a":1,"b":{"c":{"d":1}},"e":2,"f":3}',
                        ],
                        parameters=Parameters(content_type=PandasJsonContentType),
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


@pytest.mark.parametrize(
    "input, expected",
    [
        # works with params:
        (
            ['{"instances": [1, 2, 3], "params": {"foo": "bar"}}', CONTENT_TYPE_JSON],
            {"data": {"foo": [1, 2, 3]}, "params": {"foo": "bar"}},
        ),
        (
            [
                '{"inputs": [1, 2, 3], "params": {"foo": "bar"}}',
                CONTENT_TYPE_JSON,
            ],
            {"data": {"foo": [1, 2, 3]}, "params": {"foo": "bar"}},
        ),
        (
            [
                '{"inputs": {"foo": [1, 2, 3]}, "params": {"foo": "bar"}}',
                CONTENT_TYPE_JSON,
            ],
            {"data": {"foo": [1, 2, 3]}, "params": {"foo": "bar"}},
        ),
        (
            [
                '{"dataframe_split": {'
                '"columns": ["foo"], '
                '"data": [1, 2, 3]}, '
                '"params": {"foo": "bar"}}',
                CONTENT_TYPE_JSON,
            ],
            {"data": {"foo": [1, 2, 3]}, "params": {"foo": "bar"}},
        ),
        (
            [
                '{"dataframe_records": ['
                '{"foo": 1}, {"foo": 2}, {"foo": 3}], '
                '"params": {"foo": "bar"}}',
                CONTENT_TYPE_JSON,
            ],
            {"data": {"foo": [1, 2, 3]}, "params": {"foo": "bar"}},
        ),
        (
            ["foo\n1\n2\n3\n", CONTENT_TYPE_CSV],
            {"data": {"foo": [1, 2, 3]}, "params": None},
        ),
        # works without params:
        (
            ['{"instances": [1, 2, 3]}', CONTENT_TYPE_JSON],
            {"data": {"foo": [1, 2, 3]}, "params": None},
        ),
    ],
)
async def test_invocation_with_params(
    runtime: MLflowRuntime,
    input: list,
    expected: dict,
):
    with mock.patch.object(
        runtime._model, "predict", return_value=[1, 2, 3]
    ) as predict_mock:
        await runtime.invocations(*input)
        np.testing.assert_array_equal(
            predict_mock.call_args[0][0].get("foo"), expected["data"]["foo"]
        )
        assert predict_mock.call_args.kwargs["params"] == expected["params"]


@pytest.mark.parametrize(
    "input, params",
    [
        (
            InferenceRequest(
                parameters=Parameters(
                    content_type=NumpyCodec.ContentType, extra_param="extra_value"
                ),
                inputs=[
                    RequestInput(
                        name="predict",
                        shape=[1, 10],
                        data=[range(0, 10)],
                        datatype="INT64",
                        parameters=Parameters(extra_param2="extra_value2"),
                    )
                ],
            ),
            {"extra_param": "extra_value"},
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                inputs=[
                    RequestInput(
                        name="predict",
                        shape=[1, 10],
                        data=[range(0, 10)],
                        datatype="INT64",
                    )
                ],
            ),
            None,
        ),
    ],
)
async def test_predict_with_params(
    runtime: MLflowRuntime,
    input: InferenceRequest,
    params: dict,
):
    with mock.patch.object(
        runtime._model, "predict", return_value={"test": np.array([1, 2, 3])}
    ) as predict_mock:
        await runtime.predict(input)
        assert predict_mock.call_args.kwargs == {"params": params}
