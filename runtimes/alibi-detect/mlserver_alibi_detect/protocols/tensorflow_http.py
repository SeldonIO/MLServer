from .request_handler import RequestHandler
from mlserver.errors import InferenceError
import numpy as np


class TensorflowRequestHandler(RequestHandler):
    def __init__(self, request: dict):
        super().__init__(request)

    def validate(self):
        if "instances" not in self.request:
            raise InferenceError("Expected key `instances` in request body")

    def extract_request(self) -> np.array:
        return np.array(self.request["instances"])
