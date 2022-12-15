from typing import List, Any, Dict
from mlserver.codecs.base import InputCodec, register_input_codec
from mlserver.types import RequestInput, ResponseOutput, Parameters
from .utils import json_decode, json_encode


@register_input_codec
class HuggingfaceSingleJSONCodec(InputCodec):
    """
    Codec that convers to / from a JSON input.
    """

    ContentType = "hg_json"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return isinstance(payload, dict)

    @classmethod
    def encode_output(
        cls, name: str, payload: Dict[Any, Any], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:
        encoded = json_encode(payload, use_bytes)
        return ResponseOutput(
            name=name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype="BYTES",
            shape=[1],
            data=[encoded],
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> Dict[Any, Any]:
        packed = response_output.data.__root__
        return json_decode(packed[0])

    @classmethod
    def encode_input(
        cls, name: str, payload: Dict[Any, Any], use_bytes: bool = True, **kwargs
    ) -> RequestInput:
        output = cls.encode_output(name, payload, use_bytes)
        return RequestInput(
            name=output.name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[bytes]:
        packed = request_input.data.__root__
        return json_decode(packed[0])
