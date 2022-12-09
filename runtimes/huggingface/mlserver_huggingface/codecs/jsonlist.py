from typing import List, Any, Dict
from mlserver.codecs.base import InputCodec, register_input_codec
from mlserver.types import RequestInput, ResponseOutput, Parameters
from mlserver.codecs.lists import is_list_of
from functools import partial
from .utils import json_decode, json_encode


@register_input_codec
class HuggingfaceListJSONCodec(InputCodec):
    """
    Codec that convers to / from list JSON input.
    """

    ContentType = "hg_jsonlist"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, dict)

    @classmethod
    def encode_output(
        cls, name: str, payload: List[Dict[Any, Any]], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:
        packed = map(partial(json_encode, use_bytes=use_bytes), payload)
        shape = [len(payload), 1]
        return ResponseOutput(
            name=name,
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[Dict[Any, Any]]:
        packed = response_output.data.__root__
        return [json_decode(el) for el in packed]

    @classmethod
    def encode_input(
        cls, name: str, payload: List[Dict[Any, Any]], use_bytes: bool = True, **kwargs
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
    def decode_input(cls, request_input: RequestInput) -> List[Dict[Any, Any]]:
        packed = request_input.data.__root__
        return [json_decode(el) for el in packed]
