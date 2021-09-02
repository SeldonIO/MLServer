from operator import mul
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Union
from functools import reduce

from ..types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
)


def _get_data(payload: Union[RequestInput, ResponseOutput]):
    return getattr(payload.data, "__root__", payload.data)


def _infer_elem_size(shape: List[int]) -> int:
    # TODO: Allow to use a different batch dimension
    return reduce(mul, shape[1:], 1)


def _merge_data(request_inputs: List[RequestInput]) -> Any:
    all_data = [_get_data(request_input) for request_input in request_inputs]

    sampled_datum = all_data[0]

    if isinstance(sampled_datum, str):
        return "".join(all_data)

    if isinstance(sampled_datum, bytes):
        return b"".join(all_data)

    if isinstance(sampled_datum, list):
        return sum(all_data, [])

    # TODO: Should we raise an error if we couldn't merge the data?
    return all_data


def _split_data(response_output: ResponseOutput) -> Any:
    element_size = _infer_elem_size(response_output.shape)
    merged_data = _get_data(response_output)

    # TODO: Don't rely on array to have been flattened
    for i in range(0, len(merged_data), element_size):
        yield merged_data[i : i + element_size]


class BatchedRequests:
    def __init__(self, inference_requests: List[InferenceRequest] = []):
        self._inference_requests = inference_requests
        self.merged_request = self._merge_requests()
        self._prediction_ids: List[str] = [req.id for req in self._inference_requests]

    def _merge_requests(self) -> InferenceRequest:
        inputs_index: Dict[str, List[RequestInput]] = defaultdict(list)

        for inference_request in self._inference_requests:
            # TODO: What should happen if UID is empty?
            for request_input in inference_request.inputs:
                inputs_index[request_input.name].append(request_input)

        # TODO: What should happen if input cardinality is different? (e.g.
        # inputs with 2 inputs and others with 1)
        inputs = [
            self._merge_request_inputs(request_inputs)
            for request_inputs in inputs_index.values()
        ]

        # TODO: Add outputs
        # TODO: Should we add a 'fake' request ID?
        return InferenceRequest(inputs=inputs)

    def _merge_request_inputs(self, request_inputs: List[RequestInput]) -> RequestInput:
        # TODO: What should we do if list is empty?
        sampled = request_inputs[0]

        # TODO: Allow for other batch dimensions
        shape = [len(request_inputs), *sampled.shape[1:]]

        data = _merge_data(request_inputs)

        return RequestInput(
            name=sampled.name, datatype=sampled.datatype, shape=shape, data=data
        )

    def split_response(
        self, batched_response: InferenceResponse
    ) -> Iterable[InferenceResponse]:
        responses: Dict[str, InferenceResponse] = {}
        for response_output in batched_response.outputs:
            split_outputs = self._split_response_output(response_output)
            for pred_id, output in zip(self._prediction_ids, split_outputs):
                if pred_id not in responses:
                    responses[pred_id] = InferenceResponse(
                        id=pred_id, model_name=batched_response.model_name, outputs=[]
                    )

                responses[pred_id].outputs.append(output)

        return responses.values()

    def _split_response_output(
        self, response_output: ResponseOutput
    ) -> List[ResponseOutput]:
        # TODO: Support other batch dimensions
        # TODO: Support cases with multiple batch elements per input
        shape = [1, *response_output.shape[1:]]

        return [
            ResponseOutput(
                name=response_output.name,
                shape=shape,
                data=data,
                datatype=response_output.datatype,
            )
            for data in _split_data(response_output)
        ]
