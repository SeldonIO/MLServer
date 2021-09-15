import pytest

from typing import List

from mlserver.types import (
    InferenceRequest,
    RequestInput,
    ResponseOutput,
    InferenceResponse,
)
from mlserver.batching.requests import BatchedRequests


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
                    name="foo",
                    datatype="INT32",
                    shape=[2, 3],
                    data=[1, 2, 3, 10, 11, 12],
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
                shape=[4, 3],
                data=[1, 2, 3, 10, 11, 12, 4, 5, 6, 7, 8, 9],
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


@pytest.mark.parametrize(
    "minibatch_sizes, response_output, expected",
    [
        (
            [1, 1, 1],
            ResponseOutput(
                name="foo",
                datatype="INT32",
                shape=[3, 3],
                data=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            ),
            [
                ResponseOutput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[1, 2, 3]
                ),
                ResponseOutput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[4, 5, 6]
                ),
                ResponseOutput(
                    name="foo", datatype="INT32", shape=[1, 3], data=[7, 8, 9]
                ),
            ],
        ),
        (
            [1, 1, 1],
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                shape=[3, 3],
                data=b"abcdefghi",
            ),
            [
                ResponseOutput(name="foo", datatype="BYTES", shape=[1, 3], data=b"abc"),
                ResponseOutput(name="foo", datatype="BYTES", shape=[1, 3], data=b"def"),
                ResponseOutput(name="foo", datatype="BYTES", shape=[1, 3], data=b"ghi"),
            ],
        ),
        (
            [1, 2, 1],
            ResponseOutput(
                name="foo",
                datatype="BYTES",
                shape=[4, 3],
                data=b"abcdefjklghi",
            ),
            [
                ResponseOutput(name="foo", datatype="BYTES", shape=[1, 3], data=b"abc"),
                ResponseOutput(
                    name="foo", datatype="BYTES", shape=[2, 3], data=b"defjkl"
                ),
                ResponseOutput(name="foo", datatype="BYTES", shape=[1, 3], data=b"ghi"),
            ],
        ),
    ],
)
def test_split_response_output(
    minibatch_sizes: List[int],
    response_output: ResponseOutput,
    expected: List[ResponseOutput],
):
    batched = BatchedRequests()
    batched._minibatch_sizes = minibatch_sizes
    split = batched._split_response_output(response_output)

    assert list(split) == expected


@pytest.mark.parametrize(
    "minibatch_sizes, inference_response, prediction_ids, expected",
    [
        (
            [1, 1],
            InferenceResponse(
                model_name="sum-model",
                outputs=[
                    ResponseOutput(
                        name="foo",
                        datatype="INT32",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                    ),
                    ResponseOutput(
                        name="bar",
                        datatype="BYTES",
                        shape=[2, 3],
                        data=b"abcdef",
                    ),
                ],
            ),
            ["query-1", "query-2"],
            [
                InferenceResponse(
                    id="query-1",
                    model_name="sum-model",
                    outputs=[
                        ResponseOutput(
                            name="foo",
                            datatype="INT32",
                            shape=[1, 2],
                            data=[1, 2],
                        ),
                        ResponseOutput(
                            name="bar",
                            datatype="BYTES",
                            shape=[1, 3],
                            data=b"abc",
                        ),
                    ],
                ),
                InferenceResponse(
                    id="query-2",
                    model_name="sum-model",
                    outputs=[
                        ResponseOutput(
                            name="foo",
                            datatype="INT32",
                            shape=[1, 2],
                            data=[3, 4],
                        ),
                        ResponseOutput(
                            name="bar",
                            datatype="BYTES",
                            shape=[1, 3],
                            data=b"def",
                        ),
                    ],
                ),
            ],
        )
    ],
)
def test_split_response(
    minibatch_sizes: List[int],
    inference_response: InferenceResponse,
    prediction_ids: List[str],
    expected: List[InferenceResponse],
):
    batched = BatchedRequests()
    batched._prediction_ids = prediction_ids
    batched._minibatch_sizes = minibatch_sizes

    responses = batched.split_response(inference_response)
    assert list(responses) == expected
