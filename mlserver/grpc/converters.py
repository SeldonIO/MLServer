from typing import List

from . import dataplane_pb2 as pb

from .. import types


class ModelInferRequestConverter:
    @classmethod
    def to_types(cls, pb_object: pb.ModelInferRequest) -> types.InferenceRequest:
        return types.InferenceRequest(
            id=pb_object.id,
            # TODO: Add parameters,
            inputs=[
                InferInputTensorConverter.to_types(inp) for inp in pb_object.inputs
            ],
            # TODO: Add ouputs,
        )

    @classmethod
    def from_types(cls, type_object: types.InferenceRequest) -> pb.ModelInferRequest:
        pass


class InferInputTensorConverter:
    @classmethod
    def to_types(
        cls, pb_object: pb.ModelInferRequest.InferInputTensor
    ) -> types.RequestInput:
        return types.RequestInput(
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
        pass


class InferTensorContentsConverter:
    @classmethod
    def to_types(cls, pb_object: pb.InferTensorContents) -> types.TensorData:
        data = cls._get_data(pb_object)
        return types.TensorData.parse_obj(data)

    @classmethod
    def _get_data(cls, pb_object: pb.InferTensorContents) -> List:
        fields = pb_object.ListFields()
        if len(fields) == 0:
            return []

        field_name, field_value = fields[0]
        # TODO: log which field_name we are choosing
        return list(field_value)

    @classmethod
    def from_types(cls, type_object: types.TensorData) -> pb.InferTensorContents:
        pass
