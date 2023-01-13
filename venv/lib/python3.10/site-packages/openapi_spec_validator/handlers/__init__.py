from openapi_spec_validator.handlers.file import FileObjectHandler
try:
    from openapi_spec_validator.handlers.requests import (
        UrlRequestsHandler as UrlHandler,
    )
except ImportError:
    from openapi_spec_validator.handlers.urllib import (
        UrllibHandler as UrlHandler,
    )

__all__ = ['FileObjectHandler', 'UrlHandler']
