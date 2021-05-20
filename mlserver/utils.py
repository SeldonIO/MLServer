import os

from typing import List

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
