from enum import Enum
from .request_handler import RequestHandler
from .seldon_http import SeldonRequestHandler
from .tensorflow_http import TensorflowRequestHandler
from .v2 import KFservingV2RequestHandler


class Protocol(Enum):
    tensorflow_http = "tensorflow.http"
    seldon_http = "seldon.http"
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
