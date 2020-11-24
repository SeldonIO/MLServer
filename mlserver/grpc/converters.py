from typing import List

from . import dataplane_pb2 as pb
from . import model_repository_pb2 as mr_pb

from .. import types

_FIELDS = {
    "BOOL": "bool_contents",
    "UINT8": "uint_contents",
    "UINT16": "uint_contents",
    "UINT32": "uint_contents",
    "UINT64": "uint64_contents",
    "INT8": "int_contents",
    "INT16": "int_contents",
    "INT32": "int_contents",
    "INT64": "int64_contents",
    "FP16": "bytes_contents",
    "FP32": "fp32_contents",
    "FP64": "fp64_contents",
    "BYTES": "bytes_contents",
}


class ServerMetadataResponseConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ServerMetadataResponse
    ) -> types.MetadataServerResponse:
        pass

    @classmethod
    def from_types(
        cls, type_object: types.MetadataServerResponse
    ) -> pb.ServerMetadataResponse:
        return pb.ServerMetadataResponse(
            name=type_object.name,
            version=type_object.version,
            extensions=type_object.extensions,
        )


class ModelMetadataResponseConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelMetadataResponse
    ) -> types.MetadataModelResponse:
        pass

    @classmethod
    def from_types(
        cls, type_object: types.MetadataModelResponse
    ) -> pb.ModelMetadataResponse:
        metadata = pb.ModelMetadataResponse(
            name=type_object.name,
            platform=type_object.platform,
            versions=type_object.versions,
        )

        if type_object.inputs is not None:
            metadata.inputs.extend(
                [TensorMetadataConverter.from_types(inp) for inp in type_object.inputs]
            )

        if type_object.outputs is not None:
            metadata.outputs.extend(
                [TensorMetadataConverter.from_types(out) for out in type_object.outputs]
            )

        return metadata


class TensorMetadataConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelMetadataResponse.TensorMetadata
    ) -> types.MetadataTensor:
        pass

    @classmethod
    def from_types(
        cls, type_object: types.MetadataTensor
    ) -> pb.ModelMetadataResponse.TensorMetadata:
        return pb.ModelMetadataResponse.TensorMetadata(
            name=type_object.name,
            datatype=type_object.datatype,
            shape=type_object.shape,
        )


class ModelInferRequestConverter:
    @classmethod
    def to_types(cls, pb_object: pb.ModelInferRequest) -> types.InferenceRequest:
        return types.InferenceRequest.construct(
            id=pb_object.id,
            # TODO: Add parameters,
            inputs=[
                InferInputTensorConverter.to_types(inp) for inp in pb_object.inputs
            ],
            # TODO: Add ouputs,
        )

    @classmethod
    def from_types(
        cls, type_object: types.InferenceRequest, model_name: str, model_version: str
    ) -> pb.ModelInferRequest:
        return pb.ModelInferRequest(
            model_name=model_name,
            model_version=model_version,
            id=type_object.id,
            # TODO: Add parameters,
            inputs=[
                InferInputTensorConverter.from_types(inp) for inp in type_object.inputs
            ],
            # TODO: Add ouputs,
        )


class InferInputTensorConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelInferRequest.InferInputTensor
    ) -> types.RequestInput:
        return types.RequestInput.construct(
            name=pb_object.name,
            shape=list(pb_object.shape),
            datatype=pb_object.datatype,
            # TODO: Add parameters,
            data=InferTensorContentsConverter.to_types(pb_object.contents),
        )

    @classmethod
    def from_types(
        cls, type_object: types.RequestInput
    ) -> pb.ModelInferRequest.InferInputTensor:
        return pb.ModelInferRequest.InferInputTensor(
            name=type_object.name,
            shape=type_object.shape,
            datatype=type_object.datatype,
            # TODO: Add parameters,
            contents=InferTensorContentsConverter.from_types(
                type_object.data, datatype=type_object.datatype
            ),
        )


class InferTensorContentsConverter:
    @classmethod
    def to_types(cls, pb_object: pb.InferTensorContents) -> types.TensorData:
        data = cls._get_data(pb_object)
        return types.TensorData.construct(__root__=data)

    @classmethod
    def _get_data(cls, pb_object: pb.InferTensorContents) -> List:
        fields = pb_object.ListFields()
        if len(fields) == 0:
            return []

        # TODO: log which field_name we are choosing
        field_name, field_value = fields[0]
        # We return and use the pb list as-is to avoid copying the tensor
        # contents.
        return field_value

    @classmethod
    def from_types(
        cls, type_object: types.TensorData, datatype: str
    ) -> pb.InferTensorContents:
        contents = cls._get_contents(type_object, datatype)
        return pb.InferTensorContents(**contents)

    @classmethod
    def _get_contents(cls, type_object: types.TensorData, datatype: str) -> dict:
        field = _FIELDS[datatype]
        # TODO: Flatten object!
        return {field: type_object}


class ModelInferResponseConverter:
    @classmethod
    def to_types(cls, pb_object: pb.ModelInferResponse) -> types.InferenceResponse:
        pass

    @classmethod
    def from_types(cls, type_object: types.InferenceResponse) -> pb.ModelInferResponse:
        return pb.ModelInferResponse(
            model_name=type_object.model_name,
            model_version=type_object.model_version,
            id=type_object.id,
            # TODO: Add parameters
            outputs=[
                InferOutputTensorConverter.from_types(output)
                for output in type_object.outputs
            ],
        )


class InferOutputTensorConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelInferResponse.InferOutputTensor
    ) -> types.ResponseOutput:
        pass

    @classmethod
    def from_types(
        cls, type_object: types.ResponseOutput
    ) -> pb.ModelInferResponse.InferOutputTensor:
        return pb.ModelInferResponse.InferOutputTensor(
            name=type_object.name,
            shape=type_object.shape,
            datatype=type_object.datatype,
            # TODO: Add parameters
            contents=InferTensorContentsConverter.from_types(
                type_object.data, datatype=type_object.datatype
            ),
        )


class RepositoryIndexRequestConverter:
    @classmethod
    def to_types(
        cls, pb_object: mr_pb.RepositoryIndexRequest
    ) -> types.RepositoryIndexRequest:
        return types.RepositoryIndexRequest(
            ready=pb_object.ready,
        )

    @classmethod
    def from_types(
        cls, type_object: types.RepositoryIndexRequest
    ) -> mr_pb.RepositoryIndexRequest:
        raise NotImplementedError("Implement me")


class RepositoryIndexResponseConverter:
    @classmethod
    def to_types(
        cls, pb_object: mr_pb.RepositoryIndexResponse
    ) -> types.RepositoryIndexResponse:
        raise NotImplementedError("Implement me")

    @classmethod
    def from_types(
        cls, type_object: types.RepositoryIndexResponse
    ) -> mr_pb.RepositoryIndexResponse:
        return mr_pb.RepositoryIndexResponse(
            models=[
                RepositoryIndexResponseItemConverter.from_types(model)
                for model in type_object
            ]
        )


class RepositoryIndexResponseItemConverter:
    @classmethod
    def to_types(
        cls, pb_object: mr_pb.RepositoryIndexResponse.ModelIndex
    ) -> types.RepositoryIndexResponseItem:
        raise NotImplementedError("Implement me")

    @classmethod
    def from_types(
        cls, type_object: types.RepositoryIndexResponseItem
    ) -> mr_pb.RepositoryIndexResponse.ModelIndex:
        return mr_pb.RepositoryIndexResponse.ModelIndex(
            name=type_object.name,
            version=type_object.version,
            state=type_object.state.value,
            reason=type_object.reason,
        )
