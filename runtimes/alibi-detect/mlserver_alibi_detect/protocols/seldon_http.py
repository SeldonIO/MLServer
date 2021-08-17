from .request_handler import RequestHandler
from mlserver.errors import InferenceError
import numpy as np
from enum import Enum


class SeldonPayload(Enum):
    TENSOR = 1
    NDARRAY = 2
    TFTENSOR = 3


def _extract_list(body: dict) -> np.array:
    data_def = body["data"]
    if "tensor" in data_def:
        arr = np.array(data_def.get("tensor").get("values")).reshape(
            data_def.get("tensor").get("shape")
        )
        return arr
    elif "ndarray" in data_def:
        return np.array(data_def.get("ndarray"))
    elif "tftensor" in data_def:
        arr = np.array(data_def["tftensor"]["float_val"])
        shape = []
        for dim in data_def["tftensor"]["tensor_shape"]["dim"]:
            shape.append(dim["size"])
        arr = arr.reshape(shape)
        return arr
    else:
        raise Exception("Unknown Seldon payload %s" % body)


def _get_request_ty(request: dict) -> SeldonPayload:
    data_def = request["data"]
    if "tensor" in data_def:
        return SeldonPayload.TENSOR
    elif "ndarray" in data_def:
        return SeldonPayload.NDARRAY
    elif "tftensor" in data_def:
        return SeldonPayload.TFTENSOR
    else:
        raise Exception("Unknown Seldon payload %s" % data_def)


class SeldonRequestHandler(RequestHandler):
    def __init__(self, request: dict):
        super().__init__(request)

    def validate(self):
        if "data" not in self.request:
            raise InferenceError("Expected key `data` in request body")

        ty = _get_request_ty(self.request)
        if not (
            ty == SeldonPayload.TENSOR
            or ty == SeldonPayload.NDARRAY
            or ty == SeldonPayload.TFTENSOR
        ):
            raise InferenceError(
                "`data` key should contain either `tensor`,`ndarray`, or `tftensor`"
            )

    def extract_request(self) -> np.array:
        return _extract_list(self.request)
