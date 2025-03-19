# seperate file to side step circular dependency on the decode_str function

import json
import numpy as np
from typing import Any, List, Union

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore

from .string import decode_str
from .lists import as_list
from .utils import InputOrOutput


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


class JSONEncoderWithArray(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def encode_to_json(v: Any, use_bytes: bool = True) -> Union[str, bytes]:
    enc_v = json.dumps(
        v,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(",", ":"),
        cls=JSONEncoderWithArray,
    )
    if use_bytes:
        enc_v = enc_v.encode("utf-8")  # type: ignore[assignment]
    return enc_v


def decode_json_input_or_output(input_or_output: InputOrOutput) -> List[Any]:
    packed = input_or_output.data.root
    unpacked = map(json.loads, as_list(packed))
    return list(unpacked)
