import pytest

from mlserver.types import InferenceRequest
from mlserver.codecs.base import CodecError
from mlserver.codecs.utils import DefaultRequestCodec, get_decoded_or_raw


def test_default_decode(inference_request: InferenceRequest):
    inference_request.inputs = [inference_request.inputs[0]]
    first_input = DefaultRequestCodec.decode(inference_request)

    assert first_input == get_decoded_or_raw(inference_request.inputs[0])


def test_default_error(inference_request: InferenceRequest):
    with pytest.raises(CodecError):
        DefaultRequestCodec.decode(inference_request)
