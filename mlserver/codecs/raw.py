import struct

from functools import reduce
from operator import mul
from typing import List

from ..types import RequestInput, ResponseOutput

from .base import InputCodec
from .utils import InputOrOutput

_DatatypeToCtype = {
    "BOOL": "?",
    "UINT8": "B",
    "UINT16": "H",
    "UINT32": "I",
    "UINT64": "L",
    "INT8": "b",
    "INT16": "h",
    "INT32": "i",
    "INT64": "l",
    "FP16": "e",
    "FP32": "f",
    "FP64": "d",
}


def _tensor_length(shape: List[int]) -> int:
    return reduce(mul, shape, 1)


def _unpack_bytes(raw: bytes) -> List[bytes]:
    """
    From Triton's implementation:
        https://github.com/triton-inference-server/client/blob/6cc412c50ca4282cec6e9f62b3c2781be433dcc6/src/python/library/tritonclient/utils/__init__.py#L246-L273
    """
    offset = 0
    length = len(raw)
    elems = []
    while offset < length:
        [size] = struct.unpack_from("<I", raw, offset)
        offset += 4
        elem_format = f"<{size}s"
        [elem] = struct.unpack_from(elem_format, raw, offset)
        offset += size
        elems.append(elem)

    return elems


def _unpack_tensor(elem: InputOrOutput, raw: bytes) -> list:
    size = _tensor_length(elem.shape)
    ctype = _DatatypeToCtype[elem.datatype]
    form = f"{size}{ctype}"

    return list(struct.unpack(form, raw))


class RawInputCodec(InputCodec):
    @classmethod
    def _unpack(cls, elem: InputOrOutput, raw: bytes) -> InputOrOutput:
        # TODO: Assert that `data` field is empty
        if elem.datatype == "BYTES":
            elem.data = _unpack_bytes(raw)
        else:
            elem.data = _unpack_tensor(elem, raw)

        return elem

    @classmethod
    def decode_input(cls, request_input: RequestInput, raw: bytes) -> RequestInput:
        return cls._unpack(request_input, raw)

    @classmethod
    def decode_output(
        cls, response_output: ResponseOutput, raw: bytes
    ) -> ResponseOutput:
        return cls._unpack(request_input, raw)
