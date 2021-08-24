from typing import Union, Tuple, List

from mlflow.types.schema import Schema, ColSpec, TensorSpec, DataType
from mlflow.models.signature import ModelSignature

from mlserver.settings import ModelSettings
from mlserver.types import MetadataModelResponse, MetadataTensor, Tags
from mlserver.codecs import NumpyCodec, StringCodec, Base64Codec, DatetimeCodec
from mlserver.codecs.numpy import to_datatype

InputSpec = Union[ColSpec, TensorSpec]

InputDefaultPrefix = "input-"
OutputDefaultPrefix = "output-"

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
    schema: Schema, prefix=InputDefaultPrefix
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
                tags=Tags(content_type=content_type),
            )
        )

    return metadata_tensors


def to_metadata(
    signature: ModelSignature, model_settings: ModelSettings
) -> MetadataModelResponse:
    # TODO: Merge lists with existing metadata (if any) [how?]
    inputs = to_metadata_tensors(signature.inputs, prefix=InputDefaultPrefix)
    outputs = to_metadata_tensors(signature.outputs, prefix=OutputDefaultPrefix)

    return MetadataModelResponse(
        name=model_settings.name,
        platform=model_settings.platform,
        versions=model_settings.versions,
        inputs=inputs,
        outputs=outputs,
    )
