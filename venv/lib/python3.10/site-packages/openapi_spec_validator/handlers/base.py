"""OpenAPI spec validator handlers file module."""


class BaseHandler(object):
    """OpenAPI spec validator base handler."""

    def __call__(self, f):
        raise NotImplementedError
