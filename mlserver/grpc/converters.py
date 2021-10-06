from typing import Any, Union, Mapping, Optional

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


def _get_value(pb_object, default: Any = None) -> Any:
    fields = pb_object.ListFields()
    if len(fields) == 0:
        return default

    _, field_value = fields[0]
    return field_value


def _merge_map(pb_map: Mapping, value_dict: Mapping) -> Mapping:
    for key, value in value_dict.items():
        pb_map[key].MergeFrom(value)

    return pb_map


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

        if type_object.parameters is not None:
            _merge_map(
                metadata.parameters,
                ParametersConverter.from_types(type_object.parameters),  # type: ignore
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
        tensor_metadata = pb.ModelMetadataResponse.TensorMetadata(
            name=type_object.name,
            datatype=type_object.datatype,
            shape=type_object.shape,
        )

        if type_object.parameters is not None:
            _merge_map(
                tensor_metadata.parameters,
                ParametersConverter.from_types(type_object.parameters),  # type: ignore
            )

        return tensor_metadata


class ModelInferRequestConverter:
    @classmethod
    def to_types(cls, pb_object: pb.ModelInferRequest) -> types.InferenceRequest:
        inference_request = types.InferenceRequest.construct(
            id=pb_object.id,
            parameters=ParametersConverter.to_types(pb_object.parameters),
            inputs=[
                InferInputTensorConverter.to_types(inp) for inp in pb_object.inputs
            ],
        )

        if pb_object.outputs:
            inference_request.outputs = [
                InferRequestedOutputTensorConverter.to_types(out)
                for out in pb_object.outputs
            ]

        return inference_request

    @classmethod
    def from_types(
        cls, type_object: types.InferenceRequest, model_name: str, model_version: str
    ) -> pb.ModelInferRequest:
        model_infer_request = pb.ModelInferRequest(
            model_name=model_name,
            model_version=model_version,
            inputs=[
                InferInputTensorConverter.from_types(inp) for inp in type_object.inputs
            ],
        )

        if type_object.id is not None:
            model_infer_request.id = type_object.id

        if type_object.parameters is not None:
            _merge_map(
                model_infer_request.parameters,
                ParametersConverter.from_types(type_object.parameters),
            )

        if type_object.outputs is not None:
            model_infer_request.outputs.extend(
                [
                    InferRequestedOutputTensorConverter.from_types(out)
                    for out in type_object.outputs
                ]
            )

        return model_infer_request


class InferInputTensorConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelInferRequest.InferInputTensor
    ) -> types.RequestInput:
        return types.RequestInput.construct(
            name=pb_object.name,
            shape=list(pb_object.shape),
            datatype=pb_object.datatype,
            parameters=ParametersConverter.to_types(pb_object.parameters),
            data=InferTensorContentsConverter.to_types(pb_object.contents),
        )

    @classmethod
    def from_types(
        cls, type_object: types.RequestInput
    ) -> pb.ModelInferRequest.InferInputTensor:
        infer_input_tensor = pb.ModelInferRequest.InferInputTensor(
            name=type_object.name,
            shape=type_object.shape,
            datatype=type_object.datatype,
            contents=InferTensorContentsConverter.from_types(
                type_object.data, datatype=type_object.datatype
            ),
        )

        if type_object.parameters is not None:
            _merge_map(
                infer_input_tensor.parameters,
                ParametersConverter.from_types(type_object.parameters),
            )

        return infer_input_tensor


class InferRequestedOutputTensorConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelInferRequest.InferRequestedOutputTensor
    ) -> types.RequestOutput:
        return types.RequestOutput.construct(
            name=pb_object.name,
            parameters=ParametersConverter.to_types(pb_object.parameters),
        )

    @classmethod
    def from_types(
        cls, type_object: types.RequestOutput
    ) -> pb.ModelInferRequest.InferRequestedOutputTensor:
        model_infer_request = pb.ModelInferRequest.InferRequestedOutputTensor(
            name=type_object.name,
        )

        if type_object.parameters is not None:
            _merge_map(
                model_infer_request.parameters,
                ParametersConverter.from_types(type_object.parameters),
            )

        return model_infer_request


class ParametersConverter:
    @classmethod
    def to_types(
        cls, pb_object: Mapping[str, pb.InferParameter]
    ) -> Optional[types.Parameters]:
        if not pb_object:
            return None

        param_dict = {
            key: _get_value(infer_parameter)
            for key, infer_parameter in pb_object.items()
        }
        return types.Parameters(**param_dict)

    @classmethod
    def from_types(
        cls, type_object: types.Parameters
    ) -> Mapping[str, pb.InferParameter]:
        pb_object = {}
        as_dict = type_object.dict()

        for key, value in as_dict.items():
            infer_parameter_key = cls._get_inferparameter_key(value)
            if infer_parameter_key is None:
                # TODO: Log warning about ignored field
                continue

            infer_parameter = pb.InferParameter(**{infer_parameter_key: value})
            pb_object[key] = infer_parameter

        return pb_object

    @classmethod
    def _get_inferparameter_key(cls, value: Union[bool, str, int]) -> Optional[str]:
        if isinstance(value, bool):
            return "bool_param"
        elif isinstance(value, str):
            return "string_param"
        elif isinstance(value, int):
            return "int64_param"

        return None


class InferTensorContentsConverter:
    @classmethod
    def to_types(cls, pb_object: pb.InferTensorContents) -> types.TensorData:
        data = _get_value(pb_object, default=[])
        as_list = list(data)
        return types.TensorData.construct(__root__=as_list)

    @classmethod
    def from_types(
        cls, type_object: types.TensorData, datatype: str
    ) -> pb.InferTensorContents:
        contents = cls._get_contents(type_object, datatype)
        return pb.InferTensorContents(**contents)

    @classmethod
    def _get_contents(cls, type_object: types.TensorData, datatype: str) -> dict:
        field = _FIELDS[datatype]
        return {field: type_object}


class ModelInferResponseConverter:
    @classmethod
    def to_types(cls, pb_object: pb.ModelInferResponse) -> types.InferenceResponse:
        pass

    @classmethod
    def from_types(cls, type_object: types.InferenceResponse) -> pb.ModelInferResponse:
        model_infer_response = pb.ModelInferResponse(
            model_name=type_object.model_name,
            outputs=[
                InferOutputTensorConverter.from_types(output)
                for output in type_object.outputs
            ],
        )

        if type_object.model_version is not None:
            model_infer_response.model_version = type_object.model_version

        if type_object.id is not None:
            model_infer_response.id = type_object.id

        if type_object.parameters:
            _merge_map(
                model_infer_response.parameters,
                ParametersConverter.from_types(type_object.parameters),
            )

        return model_infer_response


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
        infer_output_tensor = pb.ModelInferResponse.InferOutputTensor(
            name=type_object.name,
            shape=type_object.shape,
            datatype=type_object.datatype,
            contents=InferTensorContentsConverter.from_types(
                type_object.data, datatype=type_object.datatype
            ),
        )

        if type_object.parameters:
            _merge_map(
                infer_output_tensor.parameters,
                ParametersConverter.from_types(type_object.parameters),
            )

        return infer_output_tensor


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
        model_index = mr_pb.RepositoryIndexResponse.ModelIndex(
            name=type_object.name,
            state=type_object.state.value,
            reason=type_object.reason,
        )

        if type_object.version is not None:
            model_index.version = type_object.version

        return model_index
