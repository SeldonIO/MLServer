from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Union,
    Type,
    Tuple,
    get_type_hints,
)

from ..types import InferenceRequest, InferenceResponse, RequestInput

from .base import RequestCodec, InputCodec, find_input_codec
from .errors import InputNotFound, OutputNotFound, CodecNotFound

PredictFunc = Callable[[InferenceRequest], Awaitable[InferenceResponse]]


def _as_list(a: Optional[Union[Any, Tuple[Any]]]) -> List[Any]:
    if a is None:
        return []

    if isinstance(a, tuple):
        # Split into components
        return list(a)

    # Otherwise, assume it's a single element
    return [a]


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
        self._input_hints = get_type_hints(pred)
        self._output_hints = _as_list(self._input_hints.pop("return", None))

        input_codecs = {}
        for name, type_hint in self._input_hints.items():
            codec = find_input_codec(type_hint=type_hint)
            # TODO: Consider metadata as well! (needs to be done at runtime)
            if codec is None:
                raise CodecNotFound(name=name, payload_type=type_hint, is_input=True)

            input_codecs[name] = codec

        output_codecs = []
        for type_hint in self._output_hints:
            codec = find_input_codec(type_hint=type_hint)
            if codec is None:
                raise CodecNotFound(payload_type=type_hint, is_input=False)

            output_codecs.append(codec)

        return input_codecs, output_codecs

    def decode_request(self, request: InferenceRequest) -> Dict[str, Any]:
        inputs = {}
        for request_input in request.inputs:
            input_name = request_input.name
            if input_name not in self._input_codecs:
                raise InputNotFound(input_name, self._input_codecs)

            input_codec = self._input_codecs[input_name]
            inputs[input_name] = input_codec.decode_input(request_input)

        return inputs

    def encode_response(
        self, model_name: str, payload: Any, model_version: str = None
    ) -> InferenceResponse:
        payloads = _as_list(payload)
        outputs = []
        for idx, payload in enumerate(payloads):
            output_type = type(payload)
            if idx >= len(self._output_codecs):
                raise OutputNotFound(idx, output_type, self._output_hints)

            # TODO: Fallback to encode_by_payload?
            codec = self._output_codecs[idx]
            if not codec.can_encode(payload):
                raise OutputNotFound(idx, output_type, self._output_hints)

            # TODO: Check model metadata for output names
            output_name = f"output-{idx}"
            response_output = codec.encode_output(name=output_name, payload=payload)
            outputs.append(response_output)

        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=outputs
        )


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
