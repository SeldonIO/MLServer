import json
import numpy as np
from enum import Enum
from .request_handler import RequestHandler
from .seldon_http import SeldonRequestHandler
from .tensorflow_http import TensorflowRequestHandler
from .v2 import KFservingV2RequestHandler


class Protocol(Enum):
    tensorflow_http = "tensorflow.http"
    seldon_http = "seldon.http"
    seldonfeedback_http = "seldonfeedback.http"
    kfserving_http = "kfserving.http"

    def __str__(self):
        return self.value


def get_request_handler(protocol, request: dict) -> RequestHandler:
    """
    Create a request handler for the data

    Parameters
    ----------
    protocol
         Protocol to use
    request
         The incoming request
    Returns
    -------
         A Request Handler for the desired protocol

    """
    if protocol == Protocol.tensorflow_http:
        return TensorflowRequestHandler(request)
    elif protocol == Protocol.seldon_http:
        return SeldonRequestHandler(request)
    elif protocol == Protocol.kfserving_http:
        return KFservingV2RequestHandler(request)
    else:
        raise Exception(f"Unknown protocol {protocol}")


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=arguments-differ,method-hidden
        """
        Encode Numpy Arrays as JSON
        Parameters
        ----------
        obj
             JSON Encoder

        """
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
