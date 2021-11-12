import os
import uuid

from typing import Callable, Optional, List

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

    full_model_uri = _to_absolute_path(settings._source, model_uri)
    if os.path.isfile(full_model_uri):
        return full_model_uri

    if os.path.isdir(full_model_uri):
        # If full_model_uri is a folder, search for a well-known model filename
        for fname in wellknown_filenames:
            model_path = os.path.join(full_model_uri, fname)
            if os.path.isfile(model_path):
                return model_path

        # If none, return the folder
        return full_model_uri

    # Otherwise, the uri is neither a file nor a folder
    raise InvalidModelURI(settings.name, full_model_uri)


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
