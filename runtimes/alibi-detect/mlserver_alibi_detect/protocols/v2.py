from .request_handler import RequestHandler
from mlserver.errors import InferenceError
import numpy as np


def _create_np_from_v2(data: list, ty: str, shape: list) -> np.array:
    npty = np.float
    if ty == "BOOL":
        npty = np.bool
    elif ty == "UINT8":
        npty = np.uint8
    elif ty == "UINT16":
        npty = np.uint16
    elif ty == "UINT32":
        npty = np.uint32
    elif ty == "UINT64":
        npty = np.uint64
    elif ty == "INT8":
        npty = np.int8
    elif ty == "INT16":
        npty = np.int16
    elif ty == "INT32":
        npty = np.int32
    elif ty == "INT64":
        npty = np.int64
    elif ty == "FP16":
        npty = np.float32
    elif ty == "FP32":
        npty = np.float32
    elif ty == "FP64":
        npty = np.float64
    else:
        raise InferenceError(f"V2 unknown type or type that can't be coerced {ty}")

    arr = np.array(data, dtype=npty)
    arr.shape = tuple(shape)
    return arr


class KFservingV2RequestHandler(RequestHandler):
    def __init__(self, request: dict):  # pylint: disable=useless-super-delegation
        super().__init__(request)

    def validate(self):
        if "inputs" not in self.request:
            raise InferenceError("Expected key `inputs` in request body")
        # assumes single input
        inputs = self.request["inputs"][0]
        data_type = inputs["datatype"]

        if data_type == "BYTES":
            raise InferenceError(
                "KFServing protocol BYTES data can not be presently handled"
            )

    def extract_request(self) -> np.array:
        inputs = self.request["inputs"][0]
        data_type = inputs["datatype"]
        shape = inputs["shape"]
        data = inputs["data"]
        arr = _create_np_from_v2(data, data_type, shape)
        return arr
