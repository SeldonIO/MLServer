"""OpenAPI spec validator handlers requests module."""
from __future__ import absolute_import
import contextlib

from six import StringIO
from six.moves.urllib.parse import urlparse
import requests

from openapi_spec_validator.handlers.file import FileHandler


class UrlRequestsHandler(FileHandler):
    """OpenAPI spec validator URL (requests) scheme handler."""

    def __init__(self, *allowed_schemes, **options):
        self.timeout = options.pop('timeout', 10)
        super(UrlRequestsHandler, self).__init__(**options)
        self.allowed_schemes = allowed_schemes

    def __call__(self, url):
        scheme = urlparse(url).scheme
        assert scheme in self.allowed_schemes

        if scheme == "file":
            return super(UrlRequestsHandler, self).__call__(url)

        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()

        data = StringIO(response.text)
        with contextlib.closing(data) as fh:
            return super(UrlRequestsHandler, self).__call__(fh)
