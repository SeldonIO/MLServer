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

    relative_model_uri = settings.parameters.uri
    if not relative_model_uri:
        raise InvalidModelURI(settings.name)

    model_uri = _to_absolut_path(settings._source, relative_model_uri)
    if os.path.isfile(model_uri):
        return model_uri

    if os.path.isdir(model_uri):
        # If model_uri is a folder, search for a well-known model filename
        for fname in wellknown_filenames:
            model_path = os.path.join(model_uri, fname)
            if os.path.isfile(model_path):
                return model_path

        # If none, return the folder
        return model_uri

    # Otherwise, the uri is neither a file nor a folder
    raise InvalidModelURI(settings.name, model_uri)


def _to_absolut_path(source: Optional[str], relative_model_uri: str) -> str:
    if source is None:
        return relative_model_uri

    parent_folder = os.path.dirname(source)
    unnormalised = os.path.join(parent_folder, relative_model_uri)
    return os.path.normpath(unnormalised)


def get_wrapped_method(f: Callable) -> Callable:
    while hasattr(f, "__wrapped__"):
        f = f.__wrapped__  # type: ignore

    return f


def generate_uuid() -> str:
    return str(uuid.uuid4())
