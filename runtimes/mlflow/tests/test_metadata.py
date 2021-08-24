import pytest
import numpy as np

from typing import Tuple, List

from mlflow.models.signature import ModelSignature
from mlflow.types.schema import ColSpec, TensorSpec, DataType, Schema
from mlserver.codecs import NumpyCodec, StringCodec, Base64Codec
from mlserver.types import Tags, MetadataTensor
from mlserver.settings import ModelSettings

from mlserver_mlflow.metadata import (
    InputSpec,
    InputDefaultPrefix,
    OutputDefaultPrefix,
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
            assert met.name == f"{InputDefaultPrefix}{idx}"
        else:
            assert met.name == sig.name

    assert metadata.outputs is not None
    assert len(model_signature.outputs.inputs) == len(metadata.outputs)
    for idx, met in enumerate(metadata.outputs):
        sig = model_signature.outputs.inputs[idx]

        if sig.name is None:
            assert met.name == f"{OutputDefaultPrefix}{idx}"
        else:
            assert met.name == sig.name
