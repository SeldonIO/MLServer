import asyncio

from typing import Dict
from itertools import cycle
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from asyncio import Future

from ..types import InferenceRequest, InferenceResponse
from ..utils import generate_uuid, schedule_with_callback
from ..settings import ModelSettings
from ..errors import InferenceError

from .worker import Worker
from .logging import logger
from .utils import END_OF_QUEUE, cancel_task, terminate_queue
from .messages import (
    ModelRequestMessage,
    ModelResponseMessage,
)


class Dispatcher:
    def __init__(self, workers: Dict[int, Worker], responses: Queue):
        self._responses = responses
        self._workers = workers
        self._workers_round_robin = cycle(self._workers.keys())
        self._active = False
        self._process_responses_task = None
        self._executor = ThreadPoolExecutor()
        self._async_responses: Dict[str, Future[InferenceResponse]] = {}

    def start(self):
        self._active = True
        self._process_responses_task = schedule_with_callback(
            self._process_responses(), self._process_responses_cb
        )

    def _process_responses_cb(self, process_responses):
        try:
            process_responses.result()
        except asyncio.CancelledError:
            # NOTE: The response loop was cancelled from the outside, so don't
            # restart
            return
        except Exception:
            logger.exception("Response processing loop crashed. Restarting the loop...")
            # If process loop crashed, restart it
            self.start()

    async def _process_responses(self):
        logger.debug("Starting response processing loop...")
        loop = asyncio.get_event_loop()
        while self._active:
            response = await loop.run_in_executor(self._executor, self._responses.get)

            # If the queue gets terminated, detect the "sentinel value" and
            # stop reading
            if response is END_OF_QUEUE:
                return

            await self._process_response(response)

    async def _process_response(self, response: ModelResponseMessage):
        internal_id = response.id

        async_response = self._async_responses[internal_id]

        if response.inference_response:
            async_response.set_result(response.inference_response)
        elif response.exception:
            async_response.set_exception(response.exception)
        else:
            exc = InferenceError("Inference returned no value")
            async_response.set_exception(exc)

    async def predict(
        self, model_settings: ModelSettings, inference_request: InferenceRequest
    ) -> InferenceResponse:
        internal_id = generate_uuid()

        model_version = None
        if model_settings.parameters:
            model_version = model_settings.parameters.version

        request_message = ModelRequestMessage(
            id=internal_id,
            model_name=model_settings.name,
            model_version=model_version,
            inference_request=inference_request,
        )

        worker = self._get_worker()
        worker.send_request(request_message)

        loop = asyncio.get_running_loop()
        async_response = loop.create_future()
        self._async_responses[internal_id] = async_response

        return await self._wait_response(internal_id)

    def _get_worker(self) -> Worker:
        """
        Get next available worker.
        By default, this is just a round-robin through all the workers.
        """
        worker_pid = next(self._workers_round_robin)
        return self._workers[worker_pid]

    async def _wait_response(self, internal_id: str) -> InferenceResponse:
        async_response = self._async_responses[internal_id]

        try:
            inference_response = await async_response
            return inference_response
        finally:
            del self._async_responses[internal_id]

        return await async_response

    async def stop(self):
        await terminate_queue(self._responses)
        self._responses.close()
        self._executor.shutdown()
        if self._process_responses_task is not None:
            await cancel_task(self._process_responses_task)
