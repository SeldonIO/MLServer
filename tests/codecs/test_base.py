import numpy as np
import pytest

from datetime import datetime
from typing import List, Optional

from mlserver.codecs.numpy import NumpyRequestCodec, NumpyCodec
from mlserver.codecs.string import StringRequestCodec, StringCodec
from mlserver.codecs.datetime import DatetimeCodec
from mlserver.codecs.base import _CodecRegistry, InputCodec, RequestCodec
from mlserver.types import RequestInput


@pytest.fixture
def codec_registry():
    registry = _CodecRegistry()
    registry.register_request_codec(NumpyRequestCodec.ContentType, NumpyRequestCodec)
    registry.register_request_codec(StringRequestCodec.ContentType, StringRequestCodec)
    registry.register_input_codec(NumpyCodec.ContentType, NumpyCodec)
    registry.register_input_codec(StringCodec.ContentType, StringCodec)
    registry.register_input_codec(DatetimeCodec.ContentType, DatetimeCodec)

    return registry


def test_deprecated_methods(caplog):
    request_input = RequestInput(
        name="foo", shape=[3], data=[1, 2, 3], datatype="INT32"
    )
    expected = np.array([1, 2, 3])

    decoded = NumpyCodec.decode(request_input)

    assert any(["DEPRECATED" in rec.message for rec in caplog.records])
    np.testing.assert_array_equal(decoded, expected)


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"content_type": NumpyCodec.ContentType}, NumpyCodec),
        ({"content_type": StringCodec.ContentType}, StringCodec),
        ({"content_type": "application/octet-stream"}, None),
        ({"type_hint": List[str]}, StringCodec),
        ({"type_hint": dict}, None),
        ({"payload": [datetime.now()]}, DatetimeCodec),
    ],
)
def test_find_input_codec(
    codec_registry: _CodecRegistry, kwargs: dict, expected: Optional[InputCodec]
):
    input_codec = codec_registry.find_input_codec(**kwargs)
    assert input_codec == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"content_type": NumpyRequestCodec.ContentType}, NumpyRequestCodec),
        ({"content_type": StringRequestCodec.ContentType}, StringRequestCodec),
        ({"content_type": "application/octet-stream"}, None),
        ({"type_hint": List[str]}, StringRequestCodec),
        ({"type_hint": dict}, None),
        ({"payload": ["foo"]}, StringRequestCodec),
    ],
)
def test_find_request_codec(
    codec_registry: _CodecRegistry, kwargs: dict, expected: Optional[RequestCodec]
):
    request_codec = codec_registry.find_request_codec(**kwargs)
    assert request_codec == expected
