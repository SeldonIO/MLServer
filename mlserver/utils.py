import os
import uuid
import asyncio
import urllib.parse

from asyncio import Task
from typing import Callable, Dict, Optional, List, Type

from .logging import logger
from .types import InferenceRequest, InferenceResponse, Parameters
from .settings import ModelSettings
from .errors import InvalidModelURI


async def get_model_uri(
    settings: ModelSettings, wellknown_filenames: List[str] = []
) -> str:
    if not settings.parameters:
        raise InvalidModelURI(settings.name)

    model_uri = settings.parameters.uri
    if not model_uri:
        raise InvalidModelURI(settings.name)

    model_uri_components = urllib.parse.urlparse(model_uri, scheme="file")
    if model_uri_components.scheme != "file":
        return model_uri

    full_model_path = _to_absolute_path(settings._source, model_uri_components.path)
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


def _to_absolute_path(source: Optional[str], model_uri: str) -> str:
    if source is None:
        # Treat path as either absolute or relative to the working directory of
        # the MLServer instance
        return model_uri

    parent_folder = os.path.dirname(source)
    unnormalised = os.path.join(parent_folder, model_uri)
    return os.path.normpath(unnormalised)


def get_wrapped_method(f: Callable) -> Callable:
    while hasattr(f, "__wrapped__"):
        f = f.__wrapped__  # type: ignore

    return f


def generate_uuid() -> str:
    return str(uuid.uuid4())


def insert_headers(
    inference_request: InferenceRequest, headers: Dict[str, str]
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


def extract_headers(inference_response: InferenceResponse) -> Optional[Dict[str, str]]:
    if inference_response.parameters is None:
        return None

    parameters = inference_response.parameters
    if parameters.headers is None:
        return None

    headers = parameters.headers
    parameters.headers = None
    return headers


def _check_current_event_loop_policy() -> str:
    policy = (
        "uvloop"
        if type(asyncio.get_event_loop_policy()).__module__.startswith("uvloop")
        else "asyncio"
    )
    return policy


def install_uvloop_event_loop():
    if "uvloop" == _check_current_event_loop_policy():
        return

    try:
        import uvloop

        uvloop.install()
    except ImportError:
        # else keep the standard asyncio loop as a fallback
        pass

    policy = _check_current_event_loop_policy()

    logger.debug(f"Using asyncio event-loop policy: {policy}")


def schedule_with_callback(coro, cb) -> Task:
    task = asyncio.create_task(coro)
    task.add_done_callback(cb)
    return task


def get_import_path(klass: Type):
    return f"{klass.__module__}.{klass.__name__}"
