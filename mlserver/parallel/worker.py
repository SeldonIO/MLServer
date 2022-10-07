import asyncio
import select
import signal

from asyncio import Task
from multiprocessing import Process, Queue, JoinableQueue
from concurrent.futures import ThreadPoolExecutor

from ..registry import MultiModelRegistry
from ..utils import install_uvloop_event_loop, schedule_with_callback
from ..logging import configure_logger
from ..settings import Settings

from .messages import (
    ModelRequestMessage,
    ModelUpdateType,
    ModelUpdateMessage,
    ModelResponseMessage,
)
from .utils import terminate_queue, END_OF_QUEUE
from .logging import logger

IGNORED_SIGNALS = [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]


def _noop():
    pass


class Worker(Process):
    def __init__(self, settings: Settings, responses: Queue):
        super().__init__()
        self._settings = settings
        self._responses = responses
        self._requests: Queue[ModelRequestMessage] = Queue()
        self._model_updates: JoinableQueue[ModelUpdateMessage] = JoinableQueue()

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
        configure_logger(self._settings)
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
        loop = asyncio.get_event_loop()

        while self._active:
            readable = await loop.run_in_executor(self._executor, self._select)
            for r in readable:
                if r is self._requests._reader:
                    request = self._requests.get()

                    schedule_with_callback(
                        self._process_request(request), self._request_cb
                    )
                elif r is self._model_updates._reader:
                    model_update = self._model_updates.get()
                    # If the queue gets terminated, detect the "sentinel value"
                    # and stop reading
                    if model_update is END_OF_QUEUE:
                        self._active = False
                        self._model_updates.task_done()
                        return

                    schedule_with_callback(
                        self._process_model_update(model_update), self._update_cb
                    )

    def _select(self):
        readable, _, _ = select.select(
            [self._requests._reader, self._model_updates._reader],
            [],
            [],
        )

        return readable

    async def _process_request(self, request) -> ModelResponseMessage:
        try:
            model = await self._model_registry.get_model(
                request.model_name, request.model_version
            )

            method = getattr(model, request.method_name)
            return_value = await method(*request.method_args, **request.method_kwargs)
            return ModelResponseMessage(id=request.id, return_value=return_value)
        except Exception as e:
            logger.exception(
                f"An error occurred calling method '{request.method_name}' "
                f"from model '{request.model_name}'."
            )
            return ModelResponseMessage(id=request.id, exception=e)

    def _request_cb(self, request_task: Task):
        response_message = request_task.result()
        self._responses.put(response_message)

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

    def _update_cb(self, update_task: Task):
        err = update_task.exception()
        if err:
            logger.error(err)

        self._model_updates.task_done()

    def send_request(self, request_message: ModelRequestMessage):
        """
        Send an inference request message to the worker.
        Note that this method should be both multiprocess- and thread-safe.
        """
        self._requests.put(request_message)

    async def send_update(self, model_update: ModelUpdateMessage):
        """
        Send a model update to the worker.
        Note that this method should be both multiprocess- and thread-safe.
        """
        loop = asyncio.get_event_loop()
        self._model_updates.put(model_update)
        await loop.run_in_executor(self._executor, self._model_updates.join)

    async def stop(self):
        """
        Close the worker's main loop.
        Note that this method should be both multiprocess- and thread-safe.
        """
        loop = asyncio.get_event_loop()
        await terminate_queue(self._model_updates)
        await loop.run_in_executor(self._executor, self._model_updates.join)
        self._model_updates.close()
        self._requests.close()
        self._executor.shutdown()
