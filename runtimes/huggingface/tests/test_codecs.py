import pytest
import logging
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
    Parameters,
)
from mlserver_huggingface.codecs import HuggingfaceRequestCodec


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
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str", extra={"foo3": "var2"}),
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
                ],
            ),
            {"foo": ["bar1", "bar2"], "foo2": ["var1"], "foo3": "var2"},
        ),
    ],
)
def test_decode_request(inference_request, expected):
    payload = HuggingfaceRequestCodec.decode_request(inference_request)
    assert payload == expected


@pytest.mark.parametrize(
    "inference_request, expected_payload, expected_log_msg",
    [
        (
            InferenceRequest(
                parameters=Parameters(content_type="str", extra="foo3"),
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
                ],
            ),
            {"foo": ["bar1", "bar2"]},
            logging.warn(
                "Extra parameters is provided with ",
                +"value: 'foo3' and type '<class 'str'> \n",
                +"Extra parameters cannot be parsed, expected a dictionary.",
            ),
        ),
        (
            InferenceRequest(
                parameters=Parameters(content_type="str", extra=1234),
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
                ],
            ),
            {"foo": ["bar1", "bar2"]},
            logging.warn(
                "Extra parameters is provided with "
                + "value '1234' and type '<class 'int'> \n",
                +"Extra parameters cannot be parsed, expected a dictionary.",
            ),
        ),
    ],
)
def test_decode_request_with_invalid_parameter_extra(
    inference_request, expected_payload, expected_log_msg, caplog
):
    caplog.set_level(logging.WARN)
    payload = HuggingfaceRequestCodec.decode_request(inference_request)
    assert payload == expected_payload
    assert expected_log_msg in caplog.text


@pytest.mark.parametrize(
    "payload, use_bytes, expected",
    [
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            True,
            InferenceRequest(
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=[b"bar1", b"bar2"],
                        shape=[2, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=[b"var1"],
                        shape=[1, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                ],
            ),
        ),
        (
            {"foo": ["bar1", "bar2"], "foo2": ["var1"]},
            False,
            InferenceRequest(
                model_name="my-model",
                parameters=Parameters(content_type="str"),
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="BYTES",
                        data=["bar1", "bar2"],
                        shape=[2, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                    RequestInput(
                        name="foo2",
                        datatype="BYTES",
                        data=["var1"],
                        shape=[1, 1],
                        parameters=Parameters(content_type="str"),
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_request(payload, use_bytes, expected):
    inference_request = HuggingfaceRequestCodec.encode_request(
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
    payload = HuggingfaceRequestCodec.decode_response(inference_response)

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
                        name="output_0",
                        shape=[1],
                        datatype="BYTES",
                        parameters=Parameters(content_type="hg_json"),
                        data=[b'{"foo": ["bar1", "bar2"], "foo2": ["var1"]}'],
                    )
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
                        name="output_0",
                        shape=[1],
                        datatype="BYTES",
                        parameters=Parameters(content_type="hg_json"),
                        data=['{"foo": ["bar1", "bar2"], "foo2": ["var1"]}'],
                    )
                ],
            ),
        ),
    ],
)
def test_encode_response(payload, use_bytes, expected):
    inference_response = HuggingfaceRequestCodec.encode_response(
        model_name=expected.model_name, payload=payload, use_bytes=use_bytes
    )

    assert inference_response == expected
