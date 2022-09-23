from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Tuple, get_type_hints

from ..types import InferenceRequest, InferenceResponse, RequestInput

from .base import RequestCodec, InputCodec, find_input_codec
from .errors import InputNotFound

PredictFunc = Callable[[InferenceRequest], Awaitable[InferenceResponse]]


# TODO: Should this follow the codec's interface
class SignatureCodec(RequestCodec):
    """
    Internal codec that knows how to map type hints to codecs.
    """

    # TODO: Should this receive the whole class as argument?
    def __init__(self, predict: Callable):
        self._predict = predict
        self._input_codecs, self._output_codecs = self._get_codecs(predict)

    def _get_codecs(
        self, pred: Callable
    ) -> Tuple[Dict[str, InputCodec], Tuple[InputCodec]]:
        type_hints = get_type_hints(pred)
        codecs = {}
        for name, type_hint in type_hints.items():
            codec = find_input_codec(type_hint=type_hint)
            # TODO: Raise error if codec does not exist
            # TODO: Consider metadata as well! (needs to be done at runtime)
            codecs[name] = codec

        output_codecs = codecs.pop("return", ())
        return codecs, output_codecs

    def encode_response(
        self, model_name: str, payload: Any, model_version: str = None
    ) -> InferenceResponse:
        # TODO: Deal with multiple return values
        response_outputs = [
            self._output_codecs.encode_output(name="output-0", payload=payload)
        ]
        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=response_outputs
        )

    def decode_request(self, request: InferenceRequest) -> Dict[str, Any]:
        inputs = {}
        for request_input in request.inputs:
            input_name = request_input.name
            if input_name not in self._input_codecs:
                raise InputNotFound(input_name, self._input_codecs)

            input_codec = self._input_codecs[input_name]
            inputs[input_name] = input_codec.decode_input(request_input)

        return inputs


def decode_args(predict: Callable) -> PredictFunc:
    codec = SignatureCodec(predict)

    @wraps(predict)
    async def _f(self, request: InferenceRequest) -> InferenceResponse:
        inputs = codec.decode_request(request=request)

        outputs = await predict(self, **inputs)

        return codec.encode_response(
            model_name=self.name, payload=outputs, model_version=self.version
        )

    return _f
