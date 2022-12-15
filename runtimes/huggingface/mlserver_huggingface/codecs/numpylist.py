import numpy as np

from typing import Any, List

from mlserver.types import RequestInput, ResponseOutput, Parameters

from mlserver.codecs.base import InputCodec, register_input_codec
from mlserver.codecs.utils import inject_batch_dimension
from mlserver.codecs.lists import is_list_of
from mlserver.codecs.numpy import to_datatype, _to_ndarray, _encode_data


@register_input_codec
class NumpyListCodec(InputCodec):
    """
    Encodes a tensor as a numpy array list.
    """

    ContentType = "nplist"

    @classmethod
    def can_encode(csl, payload: Any) -> bool:
        if not is_list_of(payload, np.ndarray):
            return False
        # only the support same shaped ndarray
        return len(set([matrix.shape for matrix in payload])) == 1

    @classmethod
    def encode_output(
        cls, name: str, payload: List[np.ndarray], **kwargs
    ) -> ResponseOutput:
        # NOTICE: composed np.array may cause loss of accuracy
        composed = np.array(payload)
        datatype = to_datatype(composed.dtype)
        shape = inject_batch_dimension(list(composed.shape))

        return ResponseOutput(
            name=name,
            datatype=datatype,
            shape=shape,
            data=_encode_data(composed, datatype),
            parameters=Parameters(content_type=cls.ContentType),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[np.ndarray]:
        return cls.decode_input(response_output)  # type: ignore

    @classmethod
    def encode_input(
        cls, name: str, payload: List[np.ndarray], **kwargs
    ) -> RequestInput:
        output = cls.encode_output(name=name, payload=payload)

        return RequestInput(
            name=output.name,
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
            parameters=Parameters(content_type=cls.ContentType),
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[np.ndarray]:
        model_data = _to_ndarray(request_input)
        reshaped = model_data.reshape(request_input.shape)
        return [el for el in reshaped]
