import pytest
import numpy as np

from typing import Tuple, List

from mlflow.models.signature import ModelSignature
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
    Tags,
    MetadataTensor,
    RequestInput,
    InferenceRequest,
    Parameters,
)
from mlserver.settings import ModelSettings

from mlserver_mlflow.metadata import (
    InputSpec,
    DefaultInputPrefix,
    DefaultOutputPrefix,
    _get_content_type,
    _get_shape,
    to_metadata_tensors,
    to_metadata,
)


@pytest.mark.parametrize(
    "input_spec, expected",
    [
        (
            TensorSpec(name="foo", shape=(2, 2), type=np.dtype("int32")),
            ("INT32", NumpyCodec.ContentType),
        ),
        (
            ColSpec(name="foo", type=DataType.string),
            ("BYTES", StringCodec.ContentType),
        ),
        (
            ColSpec(name="foo", type=DataType.binary),
            ("BYTES", Base64Codec.ContentType),
        ),
    ],
)
def test_get_content_type(input_spec: InputSpec, expected: Tuple[str, str]):
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
                    tags=Tags(content_type=NumpyCodec.ContentType),
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
                    tags=Tags(content_type=NumpyCodec.ContentType),
                )
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
                    tags=Tags(content_type=StringCodec.ContentType),
                ),
                MetadataTensor(
                    name="input-1",
                    datatype="INT32",
                    shape=[-1],
                    tags=Tags(content_type=NumpyCodec.ContentType),
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


def test_metadata(model_signature: ModelSignature, model_settings: ModelSettings):
    metadata = to_metadata(model_signature, model_settings)

    assert metadata.name == model_settings.name
    assert metadata.versions == model_settings.versions
    assert metadata.platform == model_settings.platform

    assert metadata.inputs is not None
    assert len(model_signature.inputs.inputs) == len(metadata.inputs)
    for idx, met in enumerate(metadata.inputs):
        sig = model_signature.inputs.inputs[idx]

        if sig.name is None:
            assert met.name == f"{DefaultInputPrefix}{idx}"
        else:
            assert met.name == sig.name

    assert metadata.outputs is not None
    assert len(model_signature.outputs.inputs) == len(metadata.outputs)
    for idx, met in enumerate(metadata.outputs):
        sig = model_signature.outputs.inputs[idx]

        if sig.name is None:
            assert met.name == f"{DefaultOutputPrefix}{idx}"
        else:
            assert met.name == sig.name
