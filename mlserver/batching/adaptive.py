import time
import asyncio

from asyncio import Future, Queue, wait_for
from typing import AsyncIterator, Awaitable, Dict, List

from ..model import MLModel
from ..types import (
    InferenceRequest,
    InferenceResponse,
)

from .requests import BatchedRequests


class AdaptiveBatcher:
    def __init__(self, model: MLModel):
        self._model = model

        self._max_batch_size = model.settings.max_batch_size
        self._max_batch_time = model.settings.max_batch_time

        # Save predict function before it gets decorated
        self._predict_fn = model.predict
        self._requests = Queue(maxsize=self._max_batch_size)
        self._async_responses: Dict[str, Future[InferenceResponse]] = {}
        self._batching_task = None

    async def predict(self, req: InferenceRequest) -> InferenceResponse:
        await self._queue_request(req)
        self._start_batcher_if_needed()
        return await self._wait_response(req)

    async def _queue_request(
        self,
        req: InferenceRequest,
    ) -> Awaitable[InferenceResponse]:
        await self._requests.put(req)

        loop = asyncio.get_running_loop()
        async_response = loop.create_future()

        # TODO: What happens if ID is None?
        self._async_responses[req.id] = async_response  # type: ignore

        return async_response

    async def _wait_response(self, req: InferenceRequest) -> InferenceResponse:
        # TODO: What happens if ID is None?
        pred_id = req.id
        async_response = self._async_responses[pred_id]

        response = await async_response

        del self._async_responses[pred_id]
        return response

    def _start_batcher_if_needed(self):
        if self._batching_task is not None:
            if not self._batching_task.done():
                # If task hasn't finished yet, let it keep running
                return

        # TODO: If _batching_task crashes, cancel all async responses
        self._batching_task = asyncio.create_task(self._batcher())

    async def _batcher(self):
        async for batched in self._batch_requests():
            batched_response = await self._predict_fn(batched.merged_request)
            responses = batched.split_response(batched_response)
            for response in responses:
                # TODO: Set error if something failed
                self._async_responses[response.id].set_result(response)

    async def _batch_requests(self) -> AsyncIterator[BatchedRequests]:
        while not self._requests.empty():
            to_batch: List[InferenceRequest] = []
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
            except asyncio.TimeoutError:
                # NOTE: Hit timeout, continue
                pass

            yield BatchedRequests(to_batch)
