import asyncio

from typing import Dict, List, Tuple
from itertools import cycle
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from asyncio import Future

from ..utils import schedule_with_callback, generate_uuid
from ..metrics import REGISTRY

from .worker import Worker
from .logging import logger
from .utils import END_OF_QUEUE, cancel_task
from .messages import (
    Message,
    ModelUpdateMessage,
    ModelRequestMessage,
    ModelResponseMessage,
)
from prometheus_client import Histogram

QUEUE_METRIC_NAME = "parallel_request_queue"


class Dispatcher:
    def __init__(self, workers: Dict[int, Worker], responses: Queue):
        self._responses = responses
        self._workers = workers
        self._workers_round_robin = cycle(self._workers.keys())
        self._active = False
        self._process_responses_task = None
        self._executor = ThreadPoolExecutor()
        self._async_responses: Dict[str, Future[ModelResponseMessage]] = {}
        self.parallel_request_queue_size = self._get_or_create_metric()

    def _get_or_create_metric(self) -> Histogram:
        if QUEUE_METRIC_NAME in REGISTRY:
            return REGISTRY[QUEUE_METRIC_NAME]  # type: ignore

        return Histogram(
            QUEUE_METRIC_NAME,
            "counter of request queue size for workers",
            registry=REGISTRY,
        )

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

        # NOTE: Use call_soon_threadsafe to cover cases where `model.predict()`
        # (or other methods) get called from a separate thread (and a separate
        # AsyncIO loop)
        response_loop = async_response.get_loop()
        if response.exception:
            response_loop.call_soon_threadsafe(
                async_response.set_exception, response.exception
            )
        else:
            response_loop.call_soon_threadsafe(async_response.set_result, response)

    async def dispatch_request(
        self, request_message: ModelRequestMessage
    ) -> ModelResponseMessage:
        worker, wpid = self._get_worker()
        worker.send_request(request_message)

        return await self._dispatch(request_message)

    def _get_worker(self) -> Tuple[Worker, int]:
        """
        Get next available worker.
        By default, this is just a round-robin through all the workers.
        """
        worker_pid = next(self._workers_round_robin)
        return self._workers[worker_pid], worker_pid

    async def dispatch_update(
        self, model_update: ModelUpdateMessage
    ) -> List[ModelResponseMessage]:
        return await asyncio.gather(
            *[
                self._dispatch_update(worker, model_update)
                for worker in self._workers.values()
            ]
        )

    async def _dispatch_update(
        self, worker: Worker, model_update: ModelUpdateMessage
    ) -> ModelResponseMessage:
        # NOTE: Need to rewrite the UUID to ensure each worker sends back a
        # unique result
        worker_update = model_update.copy()
        worker_update.id = generate_uuid()
        worker.send_update(worker_update)
        return await self._dispatch(worker_update)

    async def _dispatch(self, message: Message) -> ModelResponseMessage:
        loop = asyncio.get_running_loop()
        async_response = loop.create_future()
        internal_id = message.id
        self._async_responses[internal_id] = async_response

        # Monitor current in-flight requests
        self.parallel_request_queue_size.observe(len(self._async_responses))
        return await self._wait_response(internal_id)

    async def _wait_response(self, internal_id: str) -> ModelResponseMessage:
        async_response = self._async_responses[internal_id]

        try:
            inference_response = await async_response
            return inference_response
        finally:
            del self._async_responses[internal_id]

        return await async_response

    async def stop(self):
        self._executor.shutdown()
        if self._process_responses_task is not None:
            await cancel_task(self._process_responses_task)
