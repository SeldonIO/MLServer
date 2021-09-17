from operator import mul
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from functools import reduce

from ..types import (
    InferenceRequest,
    InferenceResponse,
    Parameters,
    RequestInput,
    ResponseOutput,
)
from .shape import Shape


def _get_data(payload: Union[RequestInput, ResponseOutput]):
    return getattr(payload.data, "__root__", payload.data)


def _merge_parameters(
    all_params: dict, parametrised_obj: Union[InferenceRequest, RequestInput]
) -> dict:
    if not parametrised_obj.parameters:
        return all_params

    obj_params = parametrised_obj.parameters.dict(exclude_unset=True)
    return {**all_params, **obj_params}


def _merge_data(
    all_data: Union[list, List[str], List[bytes]]
) -> Union[list, str, bytes]:
    sampled_datum = all_data[0]

    if isinstance(sampled_datum, str):
        return "".join(all_data)

    if isinstance(sampled_datum, bytes):
        return b"".join(all_data)

    if isinstance(sampled_datum, list):
        return sum(all_data, [])

    # TODO: Should we raise an error if we couldn't merge the data?
    return all_data


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
        all_params = {}

        for inference_request in self._inference_requests:
            all_params = _merge_parameters(all_params, inference_request)
            self._minibatch_sizes = []
            for request_input in inference_request.inputs:
                inputs_index[request_input.name].append(request_input)

        inputs = [
            self._merge_request_inputs(request_inputs)
            for request_inputs in inputs_index.values()
        ]

        # TODO: Add outputs
        # TODO: Should we add a 'fake' request ID?
        params = Parameters(**all_params) if all_params else None
        return InferenceRequest(inputs=inputs, parameters=params)

    def _merge_request_inputs(self, request_inputs: List[RequestInput]) -> RequestInput:
        self._minibatch_sizes = []
        batch_size = 0
        all_data = []
        all_params = {}
        for request_input in request_inputs:
            all_params = _merge_parameters(all_params, request_input)
            all_data.append(_get_data(request_input))
            minibatch_shape = Shape(request_input.shape)
            self._minibatch_sizes.append(minibatch_shape.batch_size)
            batch_size += minibatch_shape.batch_size

        data = _merge_data(all_data)
        parameters = Parameters(**all_params) if all_params else None

        # TODO: What should we do if list is empty?
        sampled = request_inputs[0]
        shape = Shape(sampled.shape)
        shape.batch_size = batch_size

        return RequestInput(
            name=sampled.name,
            datatype=sampled.datatype,
            shape=shape.to_list(),
            data=data,
            parameters=parameters,
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
                        id=pred_id,
                        model_name=batched_response.model_name,
                        outputs=[],
                        parameters=batched_response.parameters,
                    )

                responses[pred_id].outputs.append(output)

        return responses.values()

    def _split_response_output(
        self, response_output: ResponseOutput
    ) -> Iterable[ResponseOutput]:
        common_shape = Shape(response_output.shape)

        for minibatch_size, data in self._split_data(response_output):
            shape = common_shape.copy()
            shape.batch_size = minibatch_size
            yield ResponseOutput(
                name=response_output.name,
                shape=shape.to_list(),
                data=data,
                datatype=response_output.datatype,
                parameters=response_output.parameters,
            )

    def _split_data(self, response_output: ResponseOutput) -> Iterable[Tuple[int, Any]]:
        common_shape = Shape(response_output.shape)
        element_size = common_shape.elem_size
        merged_data = _get_data(response_output)
        idx = 0

        # TODO: Don't rely on array to have been flattened
        for minibatch_size in self._minibatch_sizes:
            data = merged_data[idx : idx + minibatch_size * element_size]
            idx += minibatch_size * element_size
            yield minibatch_size, data
