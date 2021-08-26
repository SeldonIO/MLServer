import time

from asyncio import Queue, Condition, wait_for
from typing import Dict

from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse


class AdaptiveBatching:
    def __init__(self, model: MLModel):
        # TODO: Read max_batch_size from model settings
        self._max_batch_size = 4
        self._max_batch_time = 1

        self._requests = Queue(maxsize=max_batch_size)
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
