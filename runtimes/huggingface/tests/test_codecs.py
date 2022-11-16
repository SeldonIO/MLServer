import pytest

from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
    Parameters,
)
from mlserver_huggingface.codecs import MultiStringRequestCodec


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                    ),
                    RequestInput(
                        name="foo2", datatype="BYTES", data=["var1"], shape=[1, 1]
                    ),
                ]
            ),
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
        )
    ],
)
def test_decode_request(inference_request, expected):
    payload = MultiStringRequestCodec.decode_request(inference_request)

    assert payload == expected


@pytest.mark.parametrize(
    "payload, use_bytes, expected",
    [
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            True,
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=[b"bar1", b"bar2"],
                        shape=[2, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=[b"var1"],
                        shape=[1, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                ],
            ),
        ),
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            False,
            InferenceRequest(
                model_name="my-model",
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=["var1"],
                        shape=[1, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_request(payload, use_bytes, expected):
    inference_request = MultiStringRequestCodec.encode_request(
        payload=payload, use_bytes=use_bytes
    )

    assert inference_request == expected


@pytest.mark.parametrize(
    "inference_response, expected",
    [
        (
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                    ),
                    ResponseOutput(
                        name="foo2", datatype="BYTES", data=["var1"], shape=[1, 1]
                    ),
                ],
            ),
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
        )
    ],
)
def test_decode_response(inference_response, expected):
    payload = MultiStringRequestCodec.decode_response(inference_response)

    assert payload == expected


@pytest.mark.parametrize(
    "payload, use_bytes, expected",
    [
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            True,
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="BYTES",
                        data=[b"bar1", b"bar2"],
                        shape=[2, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                    ResponseOutput(
                        name="foo2",
                        datatype="BYTES",
                        data=[b"var1"],
                        shape=[1, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                ],
            ),
        ),
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            False,
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                    ResponseOutput(
                        name="foo2",
                        datatype="BYTES",
                        data=["var1"],
                        shape=[1, 1],
                        parameters=Parameters(
                            content_type=MultiStringRequestCodec.InputCodec.ContentType
                        ),
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_response(payload, use_bytes, expected):
    inference_response = MultiStringRequestCodec.encode_response(
        model_name=expected.model_name, payload=payload, use_bytes=use_bytes
    )

    assert inference_response == expected
