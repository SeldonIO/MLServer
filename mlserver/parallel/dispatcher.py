import asyncio

from collections import defaultdict
from typing import Dict, List, Tuple, Set, Iterator
from itertools import cycle
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
from asyncio import Future

from ..utils import schedule_with_callback, generate_uuid
from ..metrics import REGISTRY

from .errors import WorkerStop
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
    def __init__(self) -> None:
        self._futures: Dict[str, Future[ModelResponseMessage]] = {}

        # _workers_map keeps track of which in-flight requests are being served
        # by each worker
        self._workers_map: Dict[int, Set[str]] = defaultdict(set)
        # _futures_map keeps track of which worker is serving each in-flight
        # request
        self._futures_map: Dict[str, int] = {}

        self.parallel_request_queue_size = self._get_or_create_metric()

    def _get_or_create_metric(self) -> Histogram:
        if QUEUE_METRIC_NAME in REGISTRY:
            return REGISTRY[QUEUE_METRIC_NAME]  # type: ignore

        return Histogram(
            QUEUE_METRIC_NAME,
            "counter of request queue size for workers",
            registry=REGISTRY,
        )

    async def schedule_and_wait(
        self, message: Message, worker: Worker
    ) -> ModelResponseMessage:
        """
        Schedule a response and wait until it gets resolved.
        """
        message_id = message.id
        self._schedule(message, worker)
        return await self._wait(message_id)

    def _schedule(self, message: Message, worker: Worker) -> Future:
        """
        Schedule a response to be resolved in the future.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        message_id = message.id
        self._futures[message_id] = future

        # Keep track of allocation for in-flight requests
        self._track_message(message, worker)

        # Monitor current in-flight requests
        in_flight_count = len(self._futures)
        self.parallel_request_queue_size.observe(in_flight_count)

        return future

    def _track_message(self, message: Message, worker: Worker) -> None:
        self._futures_map[message.id] = worker.pid  # type: ignore
        self._workers_map[worker.pid].add(message.id)  # type: ignore

    async def _wait(self, message_id: str) -> ModelResponseMessage:
        future = self._futures[message_id]

        try:
            response_message = await future
            return response_message
        finally:
            self._clear_message(message_id)

    def _clear_message(self, message_id: str) -> None:
        del self._futures[message_id]
        worker_pid = self._futures_map.pop(message_id)
        self._workers_map[worker_pid].remove(message_id)

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

    def cancel(self, worker: Worker, exit_code: int):
        """
        Cancel in-flight requests for worker (e.g. because it died
        unexpectedly).
        """
        in_flight = self._workers_map[worker.pid]  # type: ignore
        if in_flight:
            logger.info(
                f"Cancelling {len(in_flight)} in-flight requests for "
                f"worker {worker.pid} which died unexpectedly with "
                f"exit code {exit_code}..."
            )
        for message_id in in_flight:
            err = WorkerStop(exit_code)
            future = self._futures[message_id]
            loop = future.get_loop()
            loop.call_soon_threadsafe(future.set_exception, err)


class Dispatcher:
    def __init__(self, workers: Dict[int, Worker], responses: Queue):
        self._responses = responses
        self._workers = workers
        self._workers_round_robin = self._reset_round_robin()
        self._worker_starting_lock = asyncio.Lock()
        self._active = False
        self._process_responses_task = None
        self._executor = ThreadPoolExecutor()
        self._async_responses = AsyncResponses()

    def _reset_round_robin(self) -> Iterator[int]:
        worker_pids = list(self._workers.keys())
        self._workers_round_robin = cycle(worker_pids)
        return self._workers_round_robin

    async def on_worker_start(self, worker: Worker):
        """
        Handler for workers who have just started but are still not ready to
        receive traffic.
        This is used for workers that got restarted and need to reload all
        models.
        """
        # Lock while worker is coming up to ensure no model updates get lost in
        # translation
        async with self._worker_starting_lock:
            self._workers[worker.pid] = worker  # type: ignore

    def on_worker_ready(self, worker: Worker):
        """
        Handler for workers who are now ready to receive traffic.
        """
        self._reset_round_robin()

    def on_worker_stop(self, worker: Worker, exit_code: int):
        """
        Handler used for workers who stopped unexpectedly and there need to be
        removed from the round robin rotation.
        """
        pid = worker.pid
        if pid in self._workers:
            del self._workers[pid]

        self._reset_round_robin()
        self._async_responses.cancel(worker, exit_code)

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
        loop = asyncio.get_running_loop()
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

        return await self._async_responses.schedule_and_wait(request_message, worker)

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
        async with self._worker_starting_lock:
            return await asyncio.gather(
                *[
                    self.dispatch_update_to_worker(worker, model_update)
                    for worker in self._workers.values()
                ]
            )

    async def dispatch_update_to_worker(
        self, worker: Worker, model_update: ModelUpdateMessage
    ) -> ModelResponseMessage:
        # NOTE: Need to rewrite the UUID to ensure each worker sends back a
        # unique result
        worker_update = model_update.copy()
        worker_update.id = generate_uuid()
        worker.send_update(worker_update)
        return await self._async_responses.schedule_and_wait(worker_update, worker)

    async def stop(self):
        self._executor.shutdown()
        if self._process_responses_task is not None:
            await cancel_task(self._process_responses_task)
