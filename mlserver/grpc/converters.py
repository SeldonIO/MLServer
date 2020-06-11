from typing import List

from . import dataplane_pb2 as pb

from .. import types

_FIELDS = {
    "INT32": "int_contents",
    "FP32": "fp32_contents",
    # TODO: Add rest of types
}


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

        field_name, field_value = fields[0]
        # TODO: log which field_name we are choosing
        return list(field_value)

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
