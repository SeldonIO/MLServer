# seperate file to side step circular dependency on the decode_str function

import json
from functools import partial
from typing import Any, List, Union

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore

from .string import decode_str
from .lists import as_list
from .utils import InputOrOutput, SingleInputRequestCodec
from .base import InputCodec, register_input_codec, register_request_codec
from ..types import RequestInput, ResponseOutput, Parameters


# originally taken from: mlserver/rest/responses.py
class _BytesJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            # If we get a bytes payload, try to decode it back to a string on a
            # "best effort" basis
            return decode_str(obj)

        return super().default(self, obj)


def _encode_object_to_bytes(obj: Any) -> str:
    """
    Add compatibility with `bytes` payloads to `orjson`
    """
    if isinstance(obj, bytes):
        # If we get a bytes payload, try to decode it back to a string on a
        # "best effort" basis
        return decode_str(obj)

    raise TypeError


def encode_to_json_bytes(v: Any) -> bytes:
    """encodes a dict into json bytes, can deal with byte like values gracefully"""
    if orjson is None:
        # Original implementation of starlette's JSONResponse, using our
        # custom encoder (capable of "encoding" bytes).
        # Original implementation can be seen here:
        # https://github.com/encode/starlette/blob/
        # f53faba229e3fa2844bc3753e233d9c1f54cca52/starlette/responses.py#L173-L180
        return json.dumps(
            v,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=_BytesJSONEncoder,
        ).encode("utf-8")

    return orjson.dumps(v, default=_encode_object_to_bytes)


def decode_from_bytelike_json_to_dict(v: Union[bytes, str]) -> dict:
    if orjson is None:
        return json.loads(v)
    return orjson.loads(v)


def decode_input_or_output(input_or_output: InputOrOutput) -> List[Any]:
    packed = input_or_output.data.root
    unpacked = map(decode_from_bytelike_json_to_dict, as_list(packed))
    return list(unpacked)


def encode_to_json(v: Any, use_bytes: bool = True) -> Union[str, bytes]:
    enc_v = encode_to_json_bytes(v)
    if not use_bytes:
        enc_v = enc_v.decode("utf-8")  # type: ignore[union-attr, assignment]
    return enc_v


@register_input_codec
class JSONCodec(InputCodec):
    """
    Encodes a list of Python objects as a BYTES input (output).
    """

    ContentType = "json"
    TypeHint = List[Any]

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return True  # TODO: fix this

    @classmethod
    def encode_output(
        cls, name: str, payload: List[Any], use_bytes: bool = True, **kwargs
    ) -> ResponseOutput:

        packed = list(map(partial(encode_to_json, use_bytes=use_bytes), payload))
        shape = [len(payload), 1]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=packed,
            parameters=Parameters(content_type=cls.ContentType),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[Any]:
        return decode_input_or_output(response_output)

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[Any]:
        return decode_input_or_output(request_input)

    @classmethod
    def encode_input(
        cls, name: str, payload: List[Any], use_bytes: bool = True, **kwargs
    ) -> RequestInput:
        output = cls.encode_output(name, payload, use_bytes)
        return RequestInput(
            name=output.name,
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
            parameters=output.parameters,
        )


@register_request_codec
class JSONRequestCodec(SingleInputRequestCodec):
    """
    Decodes the first input (output) of request (response) as a NumPy array.
    This codec can be useful for cases where the whole payload is a single
    NumPy tensor.
    """

    InputCodec = JSONCodec
    ContentType = JSONCodec.ContentType
