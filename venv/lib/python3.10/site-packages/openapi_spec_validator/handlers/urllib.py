"""OpenAPI spec validator handlers requests module."""
import contextlib

from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import urlopen

from openapi_spec_validator.handlers.file import FileObjectHandler


class UrllibHandler(FileObjectHandler):
    """OpenAPI spec validator URL (urllib) scheme handler."""

    def __init__(self, *allowed_schemes, **options):
        self.timeout = options.pop('timeout', 10)
        super(UrllibHandler, self).__init__(**options)
        self.allowed_schemes = allowed_schemes

    def __call__(self, url):
        assert urlparse(url).scheme in self.allowed_schemes

        f = urlopen(url, timeout=self.timeout)

        with contextlib.closing(f) as fh:
            return super(UrllibHandler, self).__call__(fh)
