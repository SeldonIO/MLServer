# mypy: disable-error-code="call-arg,attr-defined"
#
# The typechecking exceptions referenced above are needed because code in this file
# dynamically considers different python versions, and some called functions are
# deprecated or take different arguments across versions.

import os
import sys
import uuid
import asyncio
from enum import Enum
from typing import cast
import warnings
import urllib.parse

from asyncio import Task
from typing import Any, Optional, TypeVar
from collections.abc import Callable, Coroutine

from .logging import logger
from .types import InferenceRequest, InferenceResponse, Parameters
from .settings import ModelSettings
from .errors import InvalidModelURI

_CoroRetT = TypeVar("_CoroRetT")
EventLoopSignalHandleConfigFn = Callable[[asyncio.AbstractEventLoop], None]
_RUN_IN_LOOP_ERROR = (
    "AsyncManager::run() cannot be called from within an existing event loop"
)


class EventLoopBackend(Enum):
    ASYNCIO_DEFAULT = 1
    UVLOOP = 2


class AsyncManager:
    def __init__(self, signal_handle_config_fn=None):
        self._event_loop_backend = EventLoopBackend.ASYNCIO_DEFAULT
        self._signal_handle_config_fn = signal_handle_config_fn
        try:
            import uvloop

            self._event_loop_backend = EventLoopBackend.UVLOOP
            self._async_run_fn = uvloop.run
        except ImportError:
            # else keep the standard asyncio loop as a fallback
            self._async_run_fn = asyncio.run
            logger.warning(
                "uvloop not available, falling back on default asyncio runner"
            )

    def _loop_factory(self) -> asyncio.AbstractEventLoop:
        new_loop: asyncio.AbstractEventLoop
        if self._event_loop_backend == EventLoopBackend.UVLOOP:
            import uvloop

            new_loop = uvloop.new_event_loop()
        else:
            new_loop = asyncio.new_event_loop()

        if self._signal_handle_config_fn is not None:
            self._signal_handle_config_fn(new_loop)

        return new_loop

    @property
    def event_loop_backend(self) -> EventLoopBackend:
        return self._event_loop_backend

    @property
    def event_loop_policy(self) -> asyncio.AbstractEventLoopPolicy:
        """
        In python versions < 3.16, return the event loop policy.
        It prefers the policy returned by uvloop where available.
        Deprecated from python 3.12, but used within pytest tests until pytest-async
        itself provides an alternative way to manage event loops across different
        python versions.
        """
        python_version_info = sys.version_info[:2]
        if python_version_info >= (3, 12):
            warnings.warn(
                "AsyncManager::event_loop_policy is deprecated since Python 3.12.",
                DeprecationWarning,
                stacklevel=1,
            )
        if python_version_info >= (3, 16):
            raise RuntimeError("EventLoopPolicy no loger supported in Python >=3.16")
        if self._event_loop_backend == EventLoopBackend.UVLOOP:
            import uvloop

            return uvloop.EventLoopPolicy()
        else:
            return cast(asyncio.AbstractEventLoopPolicy, asyncio.DefaultEventLoopPolicy)

    def run(
        self, coro: Coroutine[Any, Any, _CoroRetT], *, debug: Optional[bool] = None
    ) -> _CoroRetT:
        """
        Run a coroutine in a new event loop, and close the loop afterwards.
        Equivalent to asyncio.run(...) but with custom behaviour:

            - The event loop created during the run call is backed by uvloop when
            available, and falls back on standard the default asyncio implementation
            otherwise.
            - At the time of initialising the AsyncManager object, the resulting
            loop can also be configured with custom handlers for os signals
            (i.e SIGINT).

        This function is compatible with different python versions from 3.9 to 3.16,
        and papers over the differences in deprecated functions across these
        versions.
        """
        if self._event_loop_backend == EventLoopBackend.UVLOOP:
            # uvloop handles differences between python versions internally
            return self._async_run_fn(coro, loop_factory=self._loop_factory)

        python_version_info = sys.version_info[:2]

        if python_version_info < (3, 11):
            try:
                asyncio.get_running_loop()
                raise RuntimeError(_RUN_IN_LOOP_ERROR)
            except RuntimeError:
                pass

            if not asyncio.iscoroutine(coro):
                raise ValueError(f"expected coroutine, got {coro!r}")

            loop = self._loop_factory()
            try:
                asyncio.set_event_loop(loop)
                if debug is not None:
                    loop.set_debug(debug)
                return loop.run_until_complete(coro)
            finally:
                try:
                    _cancel_all_tasks(loop)
                    loop.run_until_complete(loop.shutdown_asyncgens())
                    if hasattr(loop, "shutdown_default_executor"):
                        loop.run_until_complete(loop.shutdown_default_executor())
                finally:
                    asyncio.set_event_loop(None)
                    loop.close()

        elif python_version_info == (3, 11):
            try:
                asyncio.get_running_loop()
                raise RuntimeError(_RUN_IN_LOOP_ERROR)
            except RuntimeError:
                pass

            with asyncio.Runner(
                loop_factory=self._loop_factory,
                debug=debug,
            ) as runner:
                return runner.run(coro)

        else:
            assert python_version_info > (3, 11)
            # From python 3.12 onwards, asyncio.run() accepts a loop_factory argument
            return asyncio.run(
                coro,
                debug=debug,
                loop_factory=self._loop_factory,
            )


def _cancel_all_tasks(loop: asyncio.AbstractEventLoop) -> None:
    # Copied from python/cpython

    to_cancel = asyncio.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(asyncio.gather(*to_cancel, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )


async def get_model_uri(
    settings: ModelSettings, wellknown_filenames: list[str] = []
) -> str:
    if not settings.parameters:
        raise InvalidModelURI(settings.name)

    model_uri = settings.parameters.uri
    if not model_uri:
        raise InvalidModelURI(settings.name)

    model_uri_components = urllib.parse.urlparse(model_uri, scheme="file")
    if model_uri_components.scheme != "file":
        return model_uri

    full_model_path = to_absolute_path(settings, model_uri_components.path)
    if os.path.isfile(full_model_path):
        return full_model_path

    if os.path.isdir(full_model_path):
        # If full_model_path is a folder, search for a well-known model filename
        for fname in wellknown_filenames:
            model_path = os.path.join(full_model_path, fname)
            if os.path.isfile(model_path):
                return model_path

        # If none, return the folder
        return full_model_path

    # Otherwise, the uri is neither a file nor a folder
    raise InvalidModelURI(settings.name, full_model_path)


def to_absolute_path(model_settings: ModelSettings, uri: str) -> str:
    source = model_settings._source
    if source is None:
        # Treat path as either absolute or relative to the working directory of
        # the MLServer instance
        return uri

    parent_folder = os.path.dirname(source)
    unnormalised = os.path.join(parent_folder, uri)
    return os.path.normpath(unnormalised)


def get_wrapped_method(f: Callable) -> Callable:
    while hasattr(f, "__wrapped__"):
        f = f.__wrapped__  # type: ignore

    return f


def generate_uuid() -> str:
    return str(uuid.uuid4())


def insert_headers(
    inference_request: InferenceRequest, headers: dict[str, str]
) -> InferenceRequest:
    # Ensure parameters are present
    if inference_request.parameters is None:
        inference_request.parameters = Parameters()

    parameters = inference_request.parameters

    if parameters.headers is not None:
        # TODO: Raise warning that headers will be replaced and shouldn't be used
        logger.warning(
            f"There are {len(parameters.headers)} entries present in the"
            "`headers` field of the request `parameters` object."
            "The `headers` field of the `parameters` object "
            "SHOULDN'T BE USED directly."
            "These entries will be replaced by the actual headers (REST, Kafka) "
            "or metadata (gRPC) of the incoming request."
        )

    parameters.headers = headers
    return inference_request


def extract_headers(inference_response: InferenceResponse) -> Optional[dict[str, str]]:
    if inference_response.parameters is None:
        return None

    parameters = inference_response.parameters
    if parameters.headers is None:
        return None

    headers = parameters.headers
    parameters.headers = None
    return headers


def schedule_with_callback(coro, cb) -> Task:
    task = asyncio.create_task(coro)
    task.add_done_callback(cb)
    return task
