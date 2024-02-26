import pytest
import numpy as np

from typing import Tuple, List

from mlflow.types.schema import ColSpec, TensorSpec, DataType, Schema
from mlflow.pyfunc import _enforce_schema
from mlserver.codecs import (
    NumpyCodec,
    StringCodec,
    Base64Codec,
    PandasCodec,
    DatetimeCodec,
    decode_inference_request,
)
from mlserver.types import (
    MetadataTensor,
    RequestInput,
    InferenceRequest,
    Parameters,
)
from mlserver.types import Datatype as MDatatype

from mlserver_mlflow.codecs import TensorDictCodec
from mlserver_mlflow.metadata import (
    InputSpec,
    _get_content_type,
    _get_shape,
    to_metadata_tensors,
    to_model_content_type,
)


@pytest.mark.parametrize(
    "input_spec, expected",
    [
        (
            TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
            (MDatatype.INT32, NumpyCodec.ContentType),
        ),
        (
            ColSpec(name="foo", type=DataType.string),
            (MDatatype.BYTES, StringCodec.ContentType),
        ),
        (
            ColSpec(name="foo", type=DataType.binary),
            (MDatatype.BYTES, Base64Codec.ContentType),
        ),
    ],
)
def test_get_content_type(input_spec: InputSpec, expected: Tuple[MDatatype, str]):
    datatype, content_type = _get_content_type(input_spec)
    assert (datatype, content_type) == expected


@pytest.mark.parametrize(
    "input_spec, expected",
    [
        (
            TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
            [2, 2],
        ),
        (
            ColSpec(name="foo", type=DataType.string),
            [-1],
        ),
    ],
)
def test_get_shape(input_spec: InputSpec, expected: List[int]):
    shape = _get_shape(input_spec)
    assert shape == expected


@pytest.mark.parametrize(
    "schema, expected",
    [
        (
            Schema(
                inputs=[TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32"))]
            ),
            [
                MetadataTensor(
                    name="foo",
                    datatype="INT32",
                    shape=[2, 2],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                )
            ],
        ),
        (
            Schema(inputs=[TensorSpec(shape=(2, 2), type=np.dtype("int32"))]),
            [
                MetadataTensor(
                    name="input-0",
                    datatype="INT32",
                    shape=[2, 2],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                )
            ],
        ),
        (
            Schema(
                inputs=[
                    TensorSpec(name="foo", shape=(-1, 2), type=np.dtype("int32")),
                    TensorSpec(name="bar", shape=(-1, 10), type=np.dtype("float32")),
                ]
            ),
            [
                MetadataTensor(
                    name="foo",
                    datatype="INT32",
                    shape=[-1, 2],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
                MetadataTensor(
                    name="bar",
                    datatype="FP32",
                    shape=[-1, 10],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
            ],
        ),
        (
            Schema(
                inputs=[
                    ColSpec(type=DataType.string),
                    ColSpec(type=DataType.integer),
                ]
            ),
            [
                MetadataTensor(
                    name="input-0",
                    datatype="BYTES",
                    shape=[-1],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
                MetadataTensor(
                    name="input-1",
                    datatype="INT32",
                    shape=[-1],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
            ],
        ),
    ],
)
def test_to_metadata_tensors(schema: Schema, expected: List[MetadataTensor]):
    metadata_tensors = to_metadata_tensors(schema)

    assert metadata_tensors == expected


@pytest.mark.parametrize(
    "tensor_spec, request_input",
    [
        (
            ColSpec(name="foo", type=DataType.boolean),
            RequestInput(
                name="foo",
                datatype="BOOL",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                shape=[2],
                data=[True, False],
            ),
        ),
        (
            ColSpec(name="foo", type=DataType.string),
            RequestInput(
                name="foo",
                datatype="BYTES",
                parameters=Parameters(content_type=StringCodec.ContentType),
                shape=[2, 11],
                data=b"hello worldhello world",
            ),
        ),
        (
            ColSpec(name="foo", type=DataType.binary),
            RequestInput(
                name="foo",
                datatype="BYTES",
                parameters=Parameters(content_type=Base64Codec.ContentType),
                shape=[1, 20],
                data=b"UHl0aG9uIGlzIGZ1bg==",
            ),
        ),
        (
            ColSpec(name="foo", type=DataType.datetime),
            RequestInput(
                name="foo",
                datatype="BYTES",
                parameters=Parameters(content_type=DatetimeCodec.ContentType),
                shape=[1, 19],
                data=b"2021-08-24T15:01:19",
            ),
        ),
    ],
)
def test_content_types(tensor_spec: TensorSpec, request_input: RequestInput):
    input_schema = Schema(inputs=[tensor_spec])

    inference_request = InferenceRequest(
        parameters=Parameters(content_type=PandasCodec.ContentType),
        inputs=[request_input],
    )
    data = decode_inference_request(inference_request)

    # _enforce_schema will raise if something fails
    _enforce_schema(data, input_schema)


@pytest.mark.parametrize(
    "schema, expected",
    [
        (
            # Expect DataFrame for named column inputs
            Schema(
                inputs=[
                    ColSpec(name="foo", type=DataType.boolean),
                    ColSpec(name="bar", type=DataType.boolean),
                ]
            ),
            PandasCodec.ContentType,
        ),
        (
            # Expect tensor dictionary for named tensor inputs
            Schema(
                inputs=[
                    TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
                    TensorSpec(name="bar", shape=(3, 2), type=np.dtype("int32")),
                ]
            ),
            TensorDictCodec.ContentType,
        ),
        (
            # Expect tensor dictionary for named tensor inputs
            Schema(
                inputs=[
                    TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
                ]
            ),
            TensorDictCodec.ContentType,
        ),
        (
            # Expect plain tensor for unnamed single tensor input
            Schema(
                inputs=[
                    TensorSpec(shape=(2, 2), type=np.dtype("int32")),
                ]
            ),
            NumpyCodec.ContentType,
        ),
    ],
)
def test_to_model_content_type(schema: Schema, expected: str):
    content_type = to_model_content_type(schema)
    assert content_type == expected
