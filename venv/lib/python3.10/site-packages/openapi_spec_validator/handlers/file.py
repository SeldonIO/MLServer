"""OpenAPI spec validator handlers file module."""
from six import StringIO
from yaml import load

from openapi_spec_validator.handlers.base import BaseHandler
from openapi_spec_validator.handlers.utils import uri_to_path
from openapi_spec_validator.loaders import ExtendedSafeLoader


class FileObjectHandler(BaseHandler):
    """OpenAPI spec validator file-like object handler."""

    def __init__(self, loader=ExtendedSafeLoader):
        self.loader = loader

    def __call__(self, f):
        return load(f, self.loader)


class FileHandler(FileObjectHandler):
    """OpenAPI spec validator file path handler."""

    def __call__(self, uri):
        if isinstance(uri, StringIO):
            return super(FileHandler, self).__call__(uri)

        assert uri.startswith("file")

        filepath = uri_to_path(uri)
        with open(filepath) as fh:
            return super(FileHandler, self).__call__(fh)
