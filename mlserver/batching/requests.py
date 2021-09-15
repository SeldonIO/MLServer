from operator import mul
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple, Union
from functools import reduce

from ..types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
)


def _get_data(payload: Union[RequestInput, ResponseOutput]):
    return getattr(payload.data, "__root__", payload.data)


def _infer_elem_size(response_output: ResponseOutput) -> int:
    batch_axis = _get_batch_axis(response_output)
    shape_without_batch = response_output.shape.copy()
    shape_without_batch.pop(batch_axis)
    return reduce(mul, shape_without_batch, 1)


def _get_batch_size(request_input: RequestInput) -> int:
    batch_dim = _get_batch_axis(request_input)
    return request_input.shape[batch_dim]


def _get_batch_axis(request_input: Union[RequestInput, ResponseOutput]) -> int:  # type: ignore
    # TODO: Support other batch dimensions
    return 0


class BatchedRequests:
    def __init__(self, inference_requests: List[InferenceRequest] = []):
        self._inference_requests = inference_requests
        self._prediction_ids: List[str] = [  # type: ignore
            req.id for req in self._inference_requests  # type: ignore
        ]
        self._minibatch_sizes: List[int] = []
        self.merged_request = self._merge_requests()

    def _merge_requests(self) -> InferenceRequest:
        inputs_index: Dict[str, List[RequestInput]] = defaultdict(list)

        for inference_request in self._inference_requests:
            # TODO: What should happen if UID is empty?
            self._minibatch_sizes = []
            for request_input in inference_request.inputs:
                inputs_index[request_input.name].append(request_input)

        inputs = [
            self._merge_request_inputs(request_inputs)
            for request_inputs in inputs_index.values()
        ]

        # TODO: Add outputs
        # TODO: Should we add a 'fake' request ID?
        return InferenceRequest(inputs=inputs)

    def _merge_request_inputs(self, request_inputs: List[RequestInput]) -> RequestInput:
        batch_size, data = self._merge_data(request_inputs)

        # TODO: What should we do if list is empty?
        sampled = request_inputs[0]

        batch_axis = _get_batch_axis(sampled)
        shape = sampled.shape.copy()
        shape.pop(batch_axis)
        shape.insert(batch_axis, batch_size)

        return RequestInput(
            name=sampled.name, datatype=sampled.datatype, shape=shape, data=data
        )

    def _merge_data(self, request_inputs: List[RequestInput]) -> Tuple[int, Any]:
        # We assume all inputs will have the same minibatch size
        self._minibatch_sizes = []
        batch_size = 0
        all_data = []
        for request_input in request_inputs:
            all_data.append(_get_data(request_input))
            minibatch_size = _get_batch_size(request_input)
            self._minibatch_sizes.append(minibatch_size)
            batch_size += minibatch_size

        sampled_datum = all_data[0]

        if isinstance(sampled_datum, str):
            return batch_size, "".join(all_data)

        if isinstance(sampled_datum, bytes):
            return batch_size, b"".join(all_data)

        if isinstance(sampled_datum, list):
            return batch_size, sum(all_data, [])

        # TODO: Should we raise an error if we couldn't merge the data?
        return batch_size, all_data

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
        batch_axis = _get_batch_axis(response_output)
        common_shape = response_output.shape.copy()

        for minibatch_size, data in self._split_data(response_output):
            shape = common_shape.copy()
            shape[batch_axis] = minibatch_size
            yield ResponseOutput(
                name=response_output.name,
                shape=shape,
                data=data,
                datatype=response_output.datatype,
            )

    def _split_data(self, response_output: ResponseOutput) -> List[Tuple[int, Any]]:
        element_size = _infer_elem_size(response_output)
        merged_data = _get_data(response_output)
        idx = 0

        # TODO: Don't rely on array to have been flattened
        for minibatch_size in self._minibatch_sizes:
            data = merged_data[idx : idx + minibatch_size * element_size]
            idx += minibatch_size * element_size
            yield minibatch_size, data
