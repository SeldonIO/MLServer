import struct

from functools import reduce
from operator import mul
from typing import List, Tuple

from .codecs.string import encode_str
from .codecs.utils import InputOrOutput
from .codecs.lists import ListElement

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

_SizeFormat = "<I"


def _tensor_length(shape: List[int]) -> int:
    return reduce(mul, shape, 1)


def _tensor_format(elem: InputOrOutput) -> str:
    size = _tensor_length(elem.shape)
    ctype = _DatatypeToCtype[elem.datatype]
    return f"{size}{ctype}"


def _unpack_bytes(raw: bytes) -> List[bytes]:
    """
    From Triton's implementation:
        https://github.com/triton-inference-server/client/blob/6cc412c50ca4282cec6e9f62b3c2781be433dcc6/src/python/library/tritonclient/utils/__init__.py#L246-L273
    """
    offset = 0
    length = len(raw)
    elems = []
    while offset < length:
        [size] = struct.unpack_from(_SizeFormat, raw, offset)
        offset += 4
        [elem] = struct.unpack_from(f"<{size}s", raw, offset)
        offset += size

        elems.append(elem)

    return elems


def _pack_bytes(unpacked: List[ListElement]) -> bytes:
    packed = []
    for elem in unpacked:
        as_bytes = _ensure_bytes(elem)
        size = len(as_bytes)

        packed_size = struct.pack(_SizeFormat, size)
        packed.append(packed_size)

        packed_elem = struct.pack(f"<{size}s", as_bytes)
        packed.append(packed_elem)

    return b"".join(packed)


def _ensure_bytes(elem: ListElement) -> bytes:
    if isinstance(elem, str):
        return encode_str(elem)

    return elem


def _unpack_tensor(elem: InputOrOutput, raw: bytes) -> list:
    tensor_format = _tensor_format(elem)
    return list(struct.unpack(tensor_format, raw))


def _pack_tensor(elem: InputOrOutput) -> bytes:
    tensor_format = _tensor_format(elem)
    return struct.pack(tensor_format, *elem.data)


def unpack(elem: InputOrOutput, raw: bytes) -> list:
    if elem.datatype == "BYTES":
        return _unpack_bytes(raw)

    return _unpack_tensor(elem, raw)


def pack(elem: InputOrOutput) -> bytes:
    if elem.datatype == "BYTES":
        return _pack_bytes(elem.data)  # type: ignore

    return _pack_tensor(elem)


def inject_raw(
    elems: List[InputOrOutput], raw_contents: List[bytes]
) -> List[InputOrOutput]:
    raw_idx = 0
    for elem in elems:
        if not elem.data:
            # Only unpack raw entry, if input / output is empty
            # This is to allow for mixed reqs / resp, where some entries have
            # data, some entries are raw
            raw = raw_contents[raw_idx]
            elem.data = unpack(elem, raw)  # type: ignore
            raw_idx += 1

    return elems


def extract_raw(elems: List[InputOrOutput]) -> Tuple[List[InputOrOutput], List[bytes]]:
    raw_contents = []
    for elem in elems:
        raw = pack(elem)
        raw_contents.append(raw)
        elem.data = []  # type: ignore

    return elems, raw_contents
