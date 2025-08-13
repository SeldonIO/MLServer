import asyncio

from collections import defaultdict
from typing import Dict, List, Tuple, Set, Iterator, AsyncIterator, Any
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
    # NEW: streaming message types
    ModelStreamChunkMessage,
    ModelStreamEndMessage,
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

        # NEW: per-request streaming queues (only for streaming calls)
        self._streams: Dict[str, asyncio.Queue] = {}

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

    # NEW: schedule without waiting (used by streaming path)
    def schedule_only(self, message: Message, worker: Worker) -> Future:
        return self._schedule(message, worker)

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
        # Clear scheduled future refs and any stream queue
        del self._futures[message_id]
        worker_pid = self._futures_map.pop(message_id)
        self._workers_map[worker_pid].remove(message_id)
        self._streams.pop(message_id, None)

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
        Cancel in-flight requests for worker (e.g. because it died unexpectedly).
        """
        in_flight = self._workers_map[worker.pid]  # type: ignore
        if in_flight:
            logger.info(
                f"Cancelling {len(in_flight)} in-flight requests for "
                f"worker {worker.pid} which died unexpectedly with "
                f"exit code {exit_code}..."
            )
        for message_id in list(in_flight):
            err = WorkerStop(exit_code)
            future = self._futures.get(message_id)
            if future is not None:
                loop = future.get_loop()
                loop.call_soon_threadsafe(future.set_exception, err)
            # Also drop any stream queue so consumers don't hang
            self._streams.pop(message_id, None)

    # -------- NEW: streaming queue helpers -----------------------------------

    def create_stream_queue(self, message_id: str, maxsize: int = 16) -> asyncio.Queue:
        """
        Create and register an asyncio.Queue used to deliver streaming messages
        for a given request id. Bounded to provide basic backpressure.
        """
        q: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self._streams[message_id] = q
        return q

    def put_stream_message(self, msg: Any) -> None:
        """
        Deliver a streaming message (chunk or end) into the per-request queue.
        """
        q = self._streams.get(msg.id)
        if q is not None:
            q.put_nowait(msg)

    def pop_stream_queue(self, message_id: str) -> None:
        self._streams.pop(message_id, None)


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
        Worker just started (not yet ready to receive traffic).
        """
        async with self._worker_starting_lock:
            self._workers[worker.pid] = worker  # type: ignore

    def on_worker_ready(self, worker: Worker):
        """
        Worker ready to receive traffic.
        """
        self._reset_round_robin()

    def on_worker_stop(self, worker: Worker, exit_code: int):
        """
        Worker stopped unexpectedly; remove from rotation and cancel in-flight.
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
            return
        except Exception:
            logger.exception("Response processing loop crashed. Restarting the loop...")
            self.start()

    async def _process_responses(self):
        logger.debug("Starting response processing loop...")
        loop = asyncio.get_event_loop()
        while self._active:
            response = await loop.run_in_executor(self._executor, self._responses.get)

            # Sentinel value -> stop
            if response is END_OF_QUEUE:
                return

            # NEW: handle streaming messages first (demux by id)
            if isinstance(response, (ModelStreamChunkMessage, ModelStreamEndMessage)):
                self._async_responses.put_stream_message(response)
                continue

            # Unary resolution
            self._async_responses.resolve(response)

    async def dispatch_request(
        self, request_message: ModelRequestMessage
    ) -> ModelResponseMessage:
        worker, _ = self._get_worker()
        worker.send_request(request_message)
        return await self._async_responses.schedule_and_wait(request_message, worker)

    # -------- NEW: streaming request path ------------------------------------

    async def dispatch_request_stream(
        self, request_message: ModelRequestMessage
    ) -> AsyncIterator[Any]:
        """
        Dispatch a request that streams multiple chunks.
        Yields chunks until END; raises if the stream ends with an exception.

        IMPORTANT: do NOT await the worker ack before yielding, or you’d block
        streaming until the end.
        """
        worker, _ = self._get_worker()

        # Create the per-request stream queue and schedule the unary future
        q = self._async_responses.create_stream_queue(request_message.id, maxsize=16)
        fut = self._async_responses.schedule_only(request_message, worker)

        # Send the request
        worker.send_request(request_message)

        # Observe the unary ack (or error) in the background without blocking
        async def _observe_ack():
            try:
                await fut
            except Exception:
                # Let worker's END carry the error if any.
                pass

        asyncio.create_task(_observe_ack())

        async def agen():
            try:
                while True:
                    msg = await q.get()
                    if isinstance(msg, ModelStreamChunkMessage):
                        yield msg.chunk
                    elif isinstance(msg, ModelStreamEndMessage):
                        if msg.exception:
                            raise msg.exception
                        break
            finally:
                # Clean up stream queue registration
                self._async_responses.pop_stream_queue(request_message.id)

        return agen()

    def _get_worker(self) -> Tuple[Worker, int]:
        """
        Round-robin selection of the next worker.
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
        worker_update = model_update.copy()
        worker_update.id = generate_uuid()
        worker.send_update(worker_update)
        return await self._async_responses.schedule_and_wait(worker_update, worker)

    async def stop(self):
        self._executor.shutdown()
        if self._process_responses_task is not None:
            await cancel_task(self._process_responses_task)