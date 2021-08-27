import pytest

from typing import List

from mlserver.model import MLModel
from mlserver.types import InferenceRequest, RequestInput
from mlserver.batching import AdaptiveBatcher, BatchedRequests


@pytest.fixture
def adaptive_batcher(sum_model: MLModel):
    return AdaptiveBatcher(sum_model)


@pytest.mark.parametrize(
    "request_inputs,expected",
    [
        (
            [
                RequestInput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[1, 2, 3]
                ),
                RequestInput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[4, 5, 6]
                ),
                RequestInput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[7, 8, 9]
                ),
            ],
            RequestInput(
                name="foo",
                datatype="INT32",
                shape=[3, 3],
                data=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            ),
        ),
        (
            [
                RequestInput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[[1, 2, 3]]
                ),
                RequestInput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[[4, 5, 6]]
                ),
                RequestInput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[[7, 8, 9]]
                ),
            ],
            RequestInput(
                name="foo",
                datatype="INT32",
                shape=[3, 3],
                data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            ),
        ),
        (
            [
                RequestInput(name="foo", datatype="BYTES", shape=[1, 3], data=b"abc"),
                RequestInput(name="foo", datatype="BYTES", shape=[1, 3], data=b"def"),
                RequestInput(name="foo", datatype="BYTES", shape=[1, 3], data=b"ghi"),
            ],
            RequestInput(
                name="foo",
                datatype="BYTES",
                shape=[3, 3],
                data=b"abcdefghi",
            ),
        ),
        (
            [
                RequestInput(name="foo", datatype="BYTES", shape=[1, 3], data="abc"),
                RequestInput(name="foo", datatype="BYTES", shape=[1, 3], data="def"),
                RequestInput(name="foo", datatype="BYTES", shape=[1, 3], data="ghi"),
            ],
            RequestInput(
                name="foo",
                datatype="BYTES",
                shape=[3, 3],
                data="abcdefghi",
            ),
        ),
    ],
)
def test_merge_request_inputs(
    request_inputs: List[RequestInput],
    expected: RequestInput,
):
    batched = BatchedRequests()
    merged = batched._merge_request_inputs(request_inputs)
    assert merged == expected


@pytest.mark.parametrize(
    "inference_requests, expected",
    [
        (
            [
                InferenceRequest(
                    inputs=[
                        RequestInput(
                            name="foo", datatype="INT32", data=[1, 2, 3], shape=[1, 3]
                        )
                    ]
                ),
                InferenceRequest(
                    inputs=[
                        RequestInput(
                            name="foo", datatype="INT32", data=[4, 5, 6], shape=[1, 3]
                        )
                    ]
                ),
            ],
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="INT32",
                        data=[1, 2, 3, 4, 5, 6],
                        shape=[2, 3],
                    )
                ]
            ),
        ),
        (
            [
                InferenceRequest(
                    inputs=[
                        RequestInput(
                            name="foo", datatype="INT32", data=[1, 2, 3], shape=[1, 3]
                        ),
                        RequestInput(
                            name="bar", datatype="BYTES", data=b"abc", shape=[1, 3]
                        ),
                    ]
                ),
                InferenceRequest(
                    inputs=[
                        RequestInput(
                            name="foo", datatype="INT32", data=[4, 5, 6], shape=[1, 3]
                        ),
                        RequestInput(
                            name="bar", datatype="BYTES", data=b"def", shape=[1, 3]
                        ),
                    ]
                ),
            ],
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo",
                        datatype="INT32",
                        data=[1, 2, 3, 4, 5, 6],
                        shape=[2, 3],
                    ),
                    RequestInput(
                        name="bar",
                        datatype="BYTES",
                        data=b"abcdef",
                        shape=[2, 3],
                    ),
                ]
            ),
        ),
    ],
)
def test_merged_request(
    inference_requests: List[InferenceRequest],
    expected: InferenceRequest,
):

    batched = BatchedRequests(inference_requests)
    merged_request = batched.merged_request

    assert merged_request == expected
