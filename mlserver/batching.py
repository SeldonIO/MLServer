import time

from asyncio import Queue, Condition, wait_for
from collections import defaultdict
from typing import Any, Dict, List

from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, RequestInput


def _get_data(request_input: RequestInput):
    return getattr(request_input.data, "__root__", request_input.data)


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


class AdaptiveBatcher:
    def __init__(self, model: MLModel):
        # TODO: Read max_batch_size from model settings
        self._max_batch_size = 4
        self._max_batch_time = 1

        self._requests = Queue(maxsize=self._max_batch_size)
        self._responses: Dict[str, InferenceResponse] = {}
        self._is_batching = Condition()

    async def predict(self, inference_request: InferenceRequest) -> InferenceResponse:
        await self._requests.put(inference_request)

        if not self._is_batching.locked():
            # If there is no admin co-routine running, start one and wait for it to
            # finish.
            await self._batch_requests()
        else:
            # Alternatively, wait for the running admin co-routine to finish.
            await self._is_batching.wait()

        # TODO: What should we do if payload has no UID?
        return self._responses.pop(inference_request.id)

    async def _batch_requests(self):
        try:
            await self._is_batching.acquire()
            to_batch = self._collect_requests()
        finally:
            self._is_batching.release()

    def _merge_requests(
        self, inference_requests: List[InferenceRequest]
    ) -> InferenceRequest:
        inputs_index: Dict[str, List[RequestInput]] = defaultdict(list)

        for inference_request in inference_requests:
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
        # TODO: What should we do if list is empty?
        sampled = request_inputs[0]

        # TODO: Allow for other batch dimensions
        shape = sampled.shape
        shape[0] = len(request_inputs)

        data = _merge_data(request_inputs)

        return RequestInput(
            name=sampled.name, datatype=sampled.datatype, shape=shape, data=data
        )

    async def _collect_requests(self):
        to_batch = []
        start = time.time()
        timeout = self._max_batch_time

        try:
            while len(to_batch) < self._max_batch_size:
                read_op = self._requests.get()
                inference_request = await wait_for(read_op, timeout=timeout)
                to_batch.append(inference_request)

                # Update remaining timeout
                current = time.time()
                timeout = timeout - (current - start)
        except TimeoutError:
            # NOTE: Hit timeout, continue
            pass

        return to_batch
