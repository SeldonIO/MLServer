from collections import defaultdict, OrderedDict
from typing import Dict, List, Optional, Union

from ..types import (
    InferenceRequest,
    InferenceResponse,
    Parameters,
    RequestInput,
    RequestOutput,
    ResponseOutput,
)
from .shape import Shape


def _get_data(payload: Union[RequestInput, ResponseOutput]):
    return getattr(payload.data, "__root__", payload.data)


def _merge_parameters(
    all_params: dict,
    parametrised_obj: Union[InferenceRequest, RequestInput, RequestOutput],
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
        return "".join(all_data)  # type: ignore

    if isinstance(sampled_datum, bytes):
        return b"".join(all_data)  # type: ignore

    if isinstance(sampled_datum, list):
        return sum(all_data, [])

    # TODO: Should we raise an error if we couldn't merge the data?
    return all_data


class BatchedRequests:
    def __init__(self, inference_requests: Dict[str, InferenceRequest] = {}):
        self.inference_requests = inference_requests

        # External IDs represent the incoming prediction IDs that need to match
        # 1:1 between request and response.
        # Since we can't ensure the uniqueness (or even presence) of the
        # external IDs, we'll also maintain our own list of internal IDs.
        self._ids_mapping: Dict[str, Optional[str]] = OrderedDict()

        # Minibatch here refers to the individual batch size of the input head
        # of each input request (i.e. the number of datapoints on each input
        # request)
        self._minibatch_sizes: Dict[str, int] = OrderedDict()

        self.merged_request = self._merge_requests()

    def _merge_requests(self) -> InferenceRequest:
        inputs_index: Dict[str, Dict[str, RequestInput]] = defaultdict(OrderedDict)
        outputs_index: Dict[str, Dict[str, RequestOutput]] = defaultdict(OrderedDict)
        all_params: dict = {}
        has_outputs = False  # if no outputs are defined, then outputs=None

        for internal_id, inference_request in self.inference_requests.items():
            self._ids_mapping[internal_id] = inference_request.id
            all_params = _merge_parameters(all_params, inference_request)
            for request_input in inference_request.inputs:
                inputs_index[request_input.name][internal_id] = request_input

            if inference_request.outputs is not None:
                has_outputs = True
                for request_output in inference_request.outputs:
                    outputs_index[request_output.name][internal_id] = request_output

        inputs = [
            self._merge_request_inputs(request_inputs)
            for request_inputs in inputs_index.values()
        ]

        outputs = (
            [
                self._merge_request_outputs(request_outputs)
                for request_outputs in outputs_index.values()
            ]
            if has_outputs
            else None
        )

        # TODO: Should we add a 'fake' request ID?
        params = Parameters(**all_params) if all_params else None
        return InferenceRequest(inputs=inputs, outputs=outputs, parameters=params)

    def _merge_request_inputs(
        self, request_inputs: Dict[str, RequestInput]
    ) -> RequestInput:
        # Note that minibatch sizes could be different on each input head,
        # however, to simplify the implementation, here we assume that it will
        # be the same across all of them
        batch_size = 0
        all_data = []
        all_params: dict = {}
        for internal_id, request_input in request_inputs.items():
            all_params = _merge_parameters(all_params, request_input)
            all_data.append(_get_data(request_input))
            minibatch_shape = Shape(request_input.shape)
            self._minibatch_sizes[internal_id] = minibatch_shape.batch_size
            batch_size += minibatch_shape.batch_size

        data = _merge_data(all_data)
        parameters = Parameters(**all_params) if all_params else None

        # TODO: What should we do if list is empty?
        sampled = next(iter(request_inputs.values()))
        shape = Shape(sampled.shape)
        shape.batch_size = batch_size

        return RequestInput(
            name=sampled.name,
            datatype=sampled.datatype,
            shape=shape.to_list(),
            data=data,
            parameters=parameters,
        )

    def _merge_request_outputs(
        self, request_outputs: Dict[str, RequestOutput]
    ) -> RequestOutput:
        all_params: dict = {}
        for internal_id, request_output in request_outputs.items():
            all_params = _merge_parameters(all_params, request_output)

        parameters = Parameters(**all_params) if all_params else None

        # TODO: What should we do if list is empty?
        sampled = next(iter(request_outputs.values()))

        return RequestOutput(name=sampled.name, parameters=parameters)

    def split_response(
        self, batched_response: InferenceResponse
    ) -> Dict[str, InferenceResponse]:
        responses: Dict[str, InferenceResponse] = {}

        for response_output in batched_response.outputs:
            response_outputs = self._split_response_output(response_output)

            for internal_id, response_output in response_outputs.items():
                if internal_id not in responses:
                    responses[internal_id] = InferenceResponse(
                        id=self._ids_mapping[internal_id],
                        model_name=batched_response.model_name,
                        model_version=batched_response.model_version,
                        outputs=[],
                        parameters=batched_response.parameters,
                    )

                responses[internal_id].outputs.append(response_output)

        return responses

    def _split_response_output(
        self, response_output: ResponseOutput
    ) -> Dict[str, ResponseOutput]:

        all_data = self._split_data(response_output)
        response_outputs = {}
        for internal_id, data in all_data.items():
            shape = Shape(response_output.shape)
            shape.batch_size = self._minibatch_sizes[internal_id]
            response_outputs[internal_id] = ResponseOutput(
                name=response_output.name,
                shape=shape.to_list(),
                data=data,
                datatype=response_output.datatype,
                parameters=response_output.parameters,
            )

        return response_outputs

    def _split_data(self, response_output: ResponseOutput) -> Dict[str, ResponseOutput]:
        merged_shape = Shape(response_output.shape)
        element_size = merged_shape.elem_size
        merged_data = _get_data(response_output)
        idx = 0

        all_data = {}
        # TODO: Don't rely on array to have been flattened
        for internal_id, minibatch_size in self._minibatch_sizes.items():
            data = merged_data[idx : idx + minibatch_size * element_size]
            idx += minibatch_size * element_size
            all_data[internal_id] = data

        return all_data
