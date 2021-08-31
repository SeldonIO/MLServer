from .request_handler import RequestHandler
from mlserver.errors import InferenceError
from mlserver.codecs import NumpyCodec
from mlserver import types
import numpy as np


class KFservingV2RequestHandler(RequestHandler):
    def __init__(self, request: dict):
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
        default_codec = NumpyCodec()
        return default_codec.decode(types.RequestInput(**inputs))
