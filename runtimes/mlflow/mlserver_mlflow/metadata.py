from typing import Union, Tuple, List, Optional

from mlflow.types.schema import Schema, ColSpec, TensorSpec, DataType

from mlserver.types import MetadataTensor, Parameters
from mlserver.codecs import (
    PandasCodec,
    NumpyCodec,
    StringCodec,
    Base64Codec,
    DatetimeCodec,
)
from mlserver.codecs.numpy import to_datatype

from .codecs import TensorDictCodec

InputSpec = Union[ColSpec, TensorSpec]

DefaultInputPrefix = "input-"
DefaultOutputPrefix = "output-"

_MLflowToContentType = {
    DataType.boolean: ("BOOL", NumpyCodec.ContentType),
    DataType.integer: ("INT32", NumpyCodec.ContentType),
    DataType.long: ("INT64", NumpyCodec.ContentType),
    DataType.float: ("FP32", NumpyCodec.ContentType),
    DataType.double: ("FP64", NumpyCodec.ContentType),
    DataType.string: ("BYTES", StringCodec.ContentType),
    DataType.binary: ("BYTES", Base64Codec.ContentType),
    DataType.datetime: ("BYTES", DatetimeCodec.ContentType),
}


def _get_content_type(input_spec: InputSpec) -> Tuple[str, str]:
    if isinstance(input_spec, TensorSpec):
        datatype = to_datatype(input_spec.type)
        content_type = NumpyCodec.ContentType
        return datatype, content_type

    # TODO: Check if new type, which may not exist
    return _MLflowToContentType[input_spec.type]


def _get_shape(input_spec: InputSpec) -> List[int]:
    if isinstance(input_spec, TensorSpec):
        return list(input_spec.shape)

    return [-1]


def to_metadata_tensors(
    schema: Schema, prefix=DefaultInputPrefix
) -> List[MetadataTensor]:
    metadata_tensors = []

    for idx, input_spec in enumerate(schema.inputs):
        datatype, content_type = _get_content_type(input_spec)
        shape = _get_shape(input_spec)

        name = input_spec.name if input_spec.name else f"{prefix}{idx}"

        metadata_tensors.append(
            MetadataTensor(
                name=name,
                datatype=datatype,
                shape=shape,
                parameters=Parameters(content_type=content_type),
            )
        )

    return metadata_tensors


def to_model_content_type(schema: Schema) -> Optional[str]:
    # This logic is based on MLflow's `mlflow.pyfunc._enforce_schema` method:
    # https://github.com/mlflow/mlflow/blob/ded7e447c20d259030260f1579693f9c5337a3ae/mlflow/pyfunc/__init__.py#L499
    if schema.is_tensor_spec():
        if schema.has_input_names():
            return TensorDictCodec.ContentType

        return NumpyCodec.ContentType

    return PandasCodec.ContentType
