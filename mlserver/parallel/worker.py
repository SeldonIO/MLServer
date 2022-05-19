import asyncio
import select
import signal

from queue import Empty
from multiprocessing import Process, Queue, JoinableQueue
from concurrent.futures import ThreadPoolExecutor

from ..registry import MultiModelRegistry
from ..utils import install_uvloop_event_loop

from .messages import ModelUpdateType, ModelUpdateMessage, InferenceResponseMessage
from .utils import terminate_queue, END_OF_QUEUE
from .logging import logger

IGNORED_SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]


def _noop():
    pass


class Worker(Process):
    def __init__(self, requests: Queue, responses: Queue):
        super().__init__()
        self._requests = requests
        self._responses = responses
        self.model_updates: JoinableQueue[ModelUpdateMessage] = JoinableQueue()

        self.__executor = None

    @property
    def _executor(self):
        """
        Helper property to initialise a threadpool executor on demand.
        This is required to avoid having to pickle the executor object into a
        separate process.
        """
        if self.__executor is None:
            self.__executor = ThreadPoolExecutor()

        return self.__executor

    def run(self):
        install_uvloop_event_loop()
        self._ignore_signals()
        asyncio.run(self.coro_run())

    def _ignore_signals(self):
        """
        Uvloop will try to propagate the main process' signals to the
        underlying workers.
        However, this would just kill off the workers without any cleaning.
        To avoid this, and be able to properly shut them down, we forcefully
        ignore the signals coming from the main parent process.
        """
        loop = asyncio.get_event_loop()

        for sign in IGNORED_SIGNALS:
            # Ensure that signal handlers are a no-op, to let the main process
            # take care of cleaning up workers
            loop.add_signal_handler(sign, _noop)

    def __inner_init__(self):
        """
        Internal __init__ method that needs to run within the worker process.
        """
        self._model_registry = MultiModelRegistry()
        self._active = True

    async def coro_run(self):
        self.__inner_init__()

        while self._active:
            readable, _, _ = select.select(
                [self._requests._reader, self.model_updates._reader],
                [],
                [],
            )
            for r in readable:
                if r is self._requests._reader:
                    try:
                        # NOTE: `select.select` will notify all workers when a
                        # new message is available. However, only one of them
                        # will be able to read it. To save us from doing more
                        # complex synchronisation, we just try to read and
                        # we'll continue if there are no messages in the queue.
                        request = self._requests.get(block=False)
                    except Empty:
                        # Some other worker got that request first, so ignore
                        # and continue
                        continue

                    await self._process_request(request)
                elif r is self.model_updates._reader:
                    model_update = self.model_updates.get()
                    # If the queue gets terminated, detect the "sentinel value"
                    # and stop reading
                    if model_update is END_OF_QUEUE:
                        self._active = False
                        self.model_updates.task_done()
                        return

                    await self._process_model_update(model_update)
                    self.model_updates.task_done()

    async def _process_request(self, request):
        try:
            model = await self._model_registry.get_model(
                request.model_name, request.model_version
            )

            inference_response = await model.predict(request.inference_request)

            response = InferenceResponseMessage(
                id=request.id, inference_response=inference_response
            )
            self._responses.put(response)
        except Exception as e:
            logger.exception("An error occurred during inference in a parallel worker.")
            exception = InferenceResponseMessage(id=request.id, exception=e)
            self._responses.put(exception)

    async def _process_model_update(self, update: ModelUpdateMessage):
        model_settings = update.model_settings
        if update.update_type == ModelUpdateType.Load:
            await self._model_registry.load(model_settings)
        elif update.update_type == ModelUpdateType.Unload:
            await self._model_registry.unload(model_settings.name)
        else:
            logger.warning(
                "Unknown model update message with type ", update.update_type
            )

    async def send_update(self, model_update: ModelUpdateMessage):
        """
        Send a model update to the worker.
        Note that this method should be both multiprocess- and thread-safe.
        """
        loop = asyncio.get_event_loop()
        self.model_updates.put(model_update)
        await loop.run_in_executor(self._executor, self.model_updates.join)

    async def stop(self):
        """
        Close the worker's main loop.
        Note that this method should be both multiprocess- and thread-safe.
        """
        loop = asyncio.get_event_loop()
        await terminate_queue(self.model_updates)
        await loop.run_in_executor(self._executor, self.model_updates.join)
        self.model_updates.close()
        self._executor.shutdown()
