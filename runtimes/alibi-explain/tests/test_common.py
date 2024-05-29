import pytest

from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
)

from mlserver_alibi_explain.common import (
    convert_from_bytes,
    remote_predict,
    SELDON_SKIP_LOGGING_HEADER,
)
from mlserver_alibi_explain.errors import InvalidExplanationShape


@pytest.mark.parametrize(
    "output",
    [
        ResponseOutput(name="foo", datatype="INT32", shape=[1, 1, 1], data=[1]),
        ResponseOutput(name="foo", datatype="INT32", shape=[1, 2], data=[1, 2]),
    ],
)
def test_convert_from_bytes_invalid(output: ResponseOutput):
    with pytest.raises(InvalidExplanationShape):
        convert_from_bytes(output)


def test_remote_predict(requests_mock):
    uri = "mock://v2/models/foo/infer"

    inference_request = InferenceRequest(
        inputs=[RequestInput(name="bar", datatype="INT32", shape=[1, 2], data=[1, 2])]
    )
    inference_response = InferenceResponse(
        model_name="foo",
        outputs=[ResponseOutput(name="bar2", datatype="FP32", shape=[1, 1], data=[3])],
    )

    requests_mock.post(
        uri,
        text=inference_response.model_dump_json(),
        request_headers={SELDON_SKIP_LOGGING_HEADER: "true"},
    )
    res = remote_predict(inference_request, uri, True)

    assert res == inference_response
