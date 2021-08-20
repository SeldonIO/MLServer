from typing import Union, Tuple

from mlflow.types.schema import ColSpec, TensorSpec, DataType
from mlserver.types import MetadataTensor, Tags
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.codecs.numpy import to_datatype

InputSpec = Union[ColSpec, TensorSpec]

_MLflowToContentType = {
    DataType.boolean: ("BOOL", NumpyCodec.ContentType),
    DataType.integer: ("INT32", NumpyCodec.ContentType),
    DataType.long: ("INT64", NumpyCodec.ContentType),
    DataType.float: ("FP32", NumpyCodec.ContentType),
    DataType.double: ("FP64", NumpyCodec.ContentType),
    DataType.string: ("BYTES", StringCodec.ContentType),
    # TODO: Add Base64 codec
    #  DataType.binary: ("BYTES", Base64Codec.ContentType),
    # TODO: Add DateTimeCodec
    #  DataType.datetime: ("BYTES", DateTimeCodec.ContentType),
}


def to_content_type(input_spec: InputSpec) -> Tuple[str, str]:
    if isinstance(input_spec, TensorSpec):
        datatype = to_datatype(input_spec.type)
        content_type = NumpyCodec.ContentType
        return datatype, content_type


def to_metadata_tensor(input_spec: InputSpec) -> MetadataTensor:
    # TODO: Can input_spec.name be None?

    datatype, tags = to_content_type(input_spec)

    return MetadataTensor(name=input_spec.name, datatype="", shape=[], tags=Tags())
