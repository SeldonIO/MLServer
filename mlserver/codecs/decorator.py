from typing import Awaitable, Callable, Dict, get_type_hints

from ..types import InferenceRequest, InferenceResponse, RequestInput
from .errors import InputNotFound

PredictFunc = Callable[[InferenceRequest], Awaitable[InferenceResponse]]


class CodecDecorator:
    """
    Internal codec that knows how to map type hints to codecs.
    """

    def __init__(self, predict: Callable):
        self._predict = predict
        self._input_hints = get_type_hints(predict)
        self._output_hints = self._input_hints.pop("return", None)

    def __call__(self, request: InferenceRequest) -> InferenceResponse:
        inputs = self._get_inputs(request)
        return None

    def _get_inputs(self, request: InferenceRequest) -> Dict[str, RequestInput]:
        inputs = {}
        for request_input in request.inputs:
            input_name = request_input.name
            if input_name not in self._input_hints:
                raise InputNotFound(input_name, self._input_hints)

            inputs[input_name] = request_input

        return inputs


def decode_args(predict: Callable) -> PredictFunc:
    return CodecDecorator(predict)
