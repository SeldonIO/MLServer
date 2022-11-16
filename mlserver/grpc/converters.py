from typing import Any, Union, Mapping, Optional

from . import dataplane_pb2 as pb
from . import model_repository_pb2 as mr_pb

from .. import types
from ..raw import extract_raw, inject_raw

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


def _get_value(pb_object, default: Optional[Any] = None) -> Any:
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
        return types.MetadataServerResponse(
            name=pb_object.name,
            version=pb_object.version,
            extensions=list(pb_object.extensions),
        )

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
        metadata = types.MetadataModelResponse(
            name=pb_object.name,
            platform=pb_object.platform,
            versions=list(pb_object.versions),
            parameters=ParametersConverter.to_types(pb_object.parameters),
        )

        if pb_object.inputs:
            metadata.inputs = [
                TensorMetadataConverter.to_types(inp) for inp in pb_object.inputs
            ]

        if pb_object.outputs:
            metadata.outputs = [
                TensorMetadataConverter.to_types(out) for out in pb_object.outputs
            ]

        return metadata

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
        return types.MetadataTensor(
            name=pb_object.name,
            datatype=pb_object.datatype,
            shape=list(pb_object.shape),
            parameters=ParametersConverter.to_types(pb_object.parameters),
        )

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

        if pb_object.raw_input_contents:
            # Unpack and inject raw contents into `data` fields if present
            inject_raw(
                inference_request.inputs, pb_object.raw_input_contents  # type: ignore
            )

        return inference_request

    @classmethod
    def from_types(
        cls,
        type_object: types.InferenceRequest,
        model_name: str,
        model_version: str = "",
        use_raw: bool = False,
    ) -> pb.ModelInferRequest:
        if use_raw:
            # Extract the raw data in advance, to ensure the `data` field of
            # the input objects is empty
            type_object.inputs, raw = extract_raw(type_object.inputs)  # type: ignore

        model_infer_request = pb.ModelInferRequest(
            model_name=model_name,
            model_version=model_version,
            inputs=[
                InferInputTensorConverter.from_types(inp) for inp in type_object.inputs
            ],
        )

        if use_raw:
            model_infer_request.raw_input_contents.extend(raw)

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
        inference_response = types.InferenceResponse.construct(
            id=pb_object.id,
            model_name=pb_object.model_name,
            parameters=ParametersConverter.to_types(pb_object.parameters),
            outputs=[
                InferOutputTensorConverter.to_types(output)
                for output in pb_object.outputs
            ],
        )

        if pb_object.model_version:
            inference_response.model_version = pb_object.model_version

        if pb_object.raw_output_contents:
            # Unpack and inject raw contents into `data` fields if present
            inject_raw(
                inference_response.outputs,  # type: ignore
                pb_object.raw_output_contents,  # type: ignore
            )

        return inference_response

    @classmethod
    def from_types(
        cls, type_object: types.InferenceResponse, use_raw: bool = False
    ) -> pb.ModelInferResponse:
        if use_raw:
            # Extract the raw data in advance, to ensure the `data` field of
            # the output objects is empty
            type_object.outputs, raw = extract_raw(type_object.outputs)  # type: ignore

        model_infer_response = pb.ModelInferResponse(
            model_name=type_object.model_name,
            outputs=[
                InferOutputTensorConverter.from_types(output)
                for output in type_object.outputs
            ],
        )

        if use_raw:
            # If using raw outputs, ensure it's set on the final object
            model_infer_response.raw_output_contents.extend(raw)

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
        return types.ResponseOutput(
            name=pb_object.name,
            shape=list(pb_object.shape),
            datatype=pb_object.datatype,
            parameters=ParametersConverter.to_types(pb_object.parameters),
            data=InferTensorContentsConverter.to_types(pb_object.contents),
        )

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
        cls, pb_object: Union[pb.RepositoryIndexRequest, mr_pb.RepositoryIndexRequest]
    ) -> types.RepositoryIndexRequest:
        return types.RepositoryIndexRequest(
            ready=pb_object.ready,
        )

    @classmethod
    def from_types(
        cls, type_object: types.RepositoryIndexRequest
    ) -> Union[pb.RepositoryIndexRequest, mr_pb.RepositoryIndexRequest]:
        raise NotImplementedError("Implement me")


class RepositoryIndexResponseConverter:
    @classmethod
    def to_types(
        cls, pb_object: Union[pb.RepositoryIndexResponse, mr_pb.RepositoryIndexResponse]
    ) -> types.RepositoryIndexResponse:
        raise NotImplementedError("Implement me")

    @classmethod
    def from_types(
        cls,
        type_object: types.RepositoryIndexResponse,
        use_model_repository: bool = False,
    ) -> Union[pb.RepositoryIndexResponse, mr_pb.RepositoryIndexResponse]:
        models = [
            RepositoryIndexResponseItemConverter.from_types(
                model, use_model_repository=use_model_repository
            )
            for model in type_object
        ]
        if use_model_repository:
            return mr_pb.RepositoryIndexResponse(models=models)  # type: ignore

        return pb.RepositoryIndexResponse(models=models)  # type: ignore


class RepositoryIndexResponseItemConverter:
    @classmethod
    def to_types(
        cls,
        pb_object: Union[
            pb.RepositoryIndexResponse.ModelIndex,
            mr_pb.RepositoryIndexResponse.ModelIndex,
        ],
    ) -> types.RepositoryIndexResponseItem:
        raise NotImplementedError("Implement me")

    @classmethod
    def from_types(
        cls,
        type_object: types.RepositoryIndexResponseItem,
        use_model_repository: bool = False,
    ) -> Union[
        pb.RepositoryIndexResponse.ModelIndex, mr_pb.RepositoryIndexResponse.ModelIndex
    ]:
        model_index = pb.RepositoryIndexResponse.ModelIndex(
            name=type_object.name,
            state=type_object.state.value,
            reason=type_object.reason,
        )

        if use_model_repository:
            model_index = mr_pb.RepositoryIndexResponse.ModelIndex(  # type: ignore
                name=type_object.name,
                state=type_object.state.value,
                reason=type_object.reason,
            )

        if type_object.version is not None:
            model_index.version = type_object.version

        return model_index
