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


class AsyncResponses:
    def __init__(self):
        self._futures: Dict[str, Future[ModelResponseMessage]] = {}
        self.parallel_request_queue_size = self._get_or_create_metric()

    def _get_or_create_metric(self) -> Histogram:
        if QUEUE_METRIC_NAME in REGISTRY:
            return REGISTRY[QUEUE_METRIC_NAME]  # type: ignore

        return Histogram(
            QUEUE_METRIC_NAME,
            "counter of request queue size for workers",
            registry=REGISTRY,
        )

    async def schedule_and_wait(self, message: Message) -> ModelResponseMessage:
        """
        Schedule a response and wait until it gets resolved.
        """
        message_id = message.id
        future = self.schedule(message)
        return await self.wait(message_id)

    def schedule(self, message: Message) -> Future:
        """
        Schedule a response to be resolved in the future.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        message_id = message.id
        self._futures[message_id] = future

        # Monitor current in-flight requests
        in_flight_count = len(self._futures)
        self.parallel_request_queue_size.observe(in_flight_count)

        return future

    async def wait(self, message_id: str) -> ModelResponseMessage:
        future = self._futures[message_id]

        try:
            response_message = await future
            return response_message
        finally:
            del self._futures[message_id]

    def resolve(self, response: ModelResponseMessage):
        """
        Resolve a previously scheduled response future.
        """
        message_id = response.id
        future = self._futures[message_id]

        # NOTE: Use call_soon_threadsafe to cover cases where `model.predict()`
        # (or other methods) get called from a separate thread (and a separate
        # AsyncIO loop)
        loop = future.get_loop()
        if response.exception:
            loop.call_soon_threadsafe(future.set_exception, response.exception)
        else:
            loop.call_soon_threadsafe(future.set_result, response)


class Dispatcher:
    def __init__(self, workers: Dict[int, Worker], responses: Queue):
        self._responses = responses
        self._workers = workers
        self._workers_round_robin = cycle(self._workers.keys())
        self._active = False
        self._process_responses_task = None
        self._executor = ThreadPoolExecutor()
        self._async_responses = AsyncResponses()

    def on_worker_stop(self, worker: Worker):
        pid = worker.pid
        if pid in self._workers:
            del self._workers[pid]

        self._workers_round_robin = cycle(self._workers.keys())

        # TODO: Cancel on-flight requests for worker?

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

            self._async_responses.resolve(response)

    async def dispatch_request(
        self, request_message: ModelRequestMessage
    ) -> ModelResponseMessage:
        worker, wpid = self._get_worker()
        worker.send_request(request_message)

        return await self._async_responses.schedule_and_wait(request_message)

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
        return await self._async_responses.schedule_and_wait(worker_update)

    async def stop(self):
        self._executor.shutdown()
        if self._process_responses_task is not None:
            await cancel_task(self._process_responses_task)
