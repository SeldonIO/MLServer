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

from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput

from .base import RequestCodec, InputCodec, find_input_codec, find_request_codec
from .errors import InputsNotFound, OutputNotFound, CodecNotFound
from .utils import Codec

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

    def _get_codecs(self, pred: Callable) -> Tuple[Dict[str, Codec], Tuple[Codec]]:
        self._input_hints = get_type_hints(pred)
        self._output_hints = _as_list(self._input_hints.pop("return", None))

        input_codecs = {}
        for name, type_hint in self._input_hints.items():
            codec = self._find_codec(name=name, type_hint=type_hint, is_input=True)
            # TODO: Consider metadata as well! (needs to be done at runtime)
            input_codecs[name] = codec

        output_codecs = []
        for type_hint in self._output_hints:
            # Try either as an input or as a request codec
            codec = self._find_codec(name=None, type_hint=type_hint, is_input=False)
            output_codecs.append(codec)

        return input_codecs, output_codecs

    def _find_codec(
        self, name: Optional[str], type_hint: Type, is_input: bool = False
    ) -> Codec:
        codec = find_input_codec(type_hint=type_hint)
        if codec is not None:
            return codec

        codec = find_request_codec(type_hint=type_hint)
        if codec is not None:
            return codec

        raise CodecNotFound(name=name, payload_type=type_hint, is_input=is_input)

    def decode_request(self, request: InferenceRequest) -> Dict[str, Any]:
        inputs = {}
        extra_request_inputs = []
        for request_input in request.inputs:
            input_name = request_input.name
            if input_name not in self._input_codecs:
                # Aggregate extra request inputs to check later, as they could
                # be part of aggregated request codecs (e.g. like dataframes)
                extra_request_inputs.append(request_input)
                continue

            # Ensure matching codec is an input codec
            codec = self._input_codecs[input_name]
            if not issubclass(codec, InputCodec):
                raise CodecNotFound(name=input_name, is_input=True)

            inputs[input_name] = codec.decode_input(request_input)

        if extra_request_inputs:
            request_codec = self._get_request_codec()
            if not request_codec:
                # If there are no request codecs that can aggregate all
                # remaining inputs, raise an error
                raise InputsNotFound(extra_request_inputs, self._input_codecs)

            # We create a fake request built from the extra request inputs
            name, codec = request_codec
            extra_inputs = InferenceRequest(inputs=extra_request_inputs)
            inputs[name] = codec.decode_request(extra_inputs)

        return inputs

    def _get_request_codec(self) -> Optional[Tuple[str, RequestCodec]]:
        for name, codec in self._input_codecs.items():
            if issubclass(codec, RequestCodec):
                return name, codec

    def encode_response(
        self, model_name: str, payload: Any, model_version: str = None
    ) -> InferenceResponse:
        payloads = _as_list(payload)
        outputs = []
        for idx, payload in enumerate(payloads):
            outputs += self._encode_outputs(idx, payload)

        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=outputs
        )

    def _encode_outputs(self, idx: int, payload: Any) -> List[ResponseOutput]:
        output_type = type(payload)
        if idx >= len(self._output_codecs):
            raise OutputNotFound(idx, output_type, self._output_hints)

        # TODO: Fallback to encode_by_payload?
        codec = self._output_codecs[idx]
        if not codec.can_encode(payload):
            raise OutputNotFound(idx, output_type, self._output_hints)

        if issubclass(codec, InputCodec):
            # TODO: Check model metadata for output names
            output_name = f"output-{idx}"
            response_output = codec.encode_output(name=output_name, payload=payload)
            return [response_output]

        if issubclass(codec, RequestCodec):
            # NOTE: We will ignore `model_name` and only grab the outputs
            response = codec.encode_response(model_name="", payload=payload)
            return response.outputs

        return []


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
