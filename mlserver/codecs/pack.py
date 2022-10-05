import struct

from functools import reduce
from operator import mul
from typing import List

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


def unpack_bytes(raw: bytes) -> List[bytes]:
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


def unpack_tensor(elem: InputOrOutput, raw: bytes) -> list:
    size = _tensor_length(elem.shape)
    ctype = _DatatypeToCtype[elem.datatype]
    form = f"{size}{ctype}"

    return list(struct.unpack(form, raw))


def unpack(elem: InputOrOutput, raw: bytes) -> list:
    if elem.datatype == "BYTES":
        return unpack_bytes(raw)

    return unpack_tensor(elem, raw)
