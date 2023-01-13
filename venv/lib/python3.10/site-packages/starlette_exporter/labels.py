"""utilities for working with labels"""
from typing import Callable, Iterable, Optional

from starlette.requests import Request


def from_header(key: str, allowed_values: Optional[Iterable] = None) -> Callable:
    """returns a function that retrieves a header value from a request.
    The returned function can be passed to the `labels` argument of PrometheusMiddleware
    to label metrics using a header value.

    `key`: header key
    `allowed_values`: an iterable (e.g. list or tuple) containing an allowlist of values. Any
    header value not in allowed_values will result in an empty string being returned.  Use
    this to constrain the potential label values.

    example:

    ```
        PrometheusMiddleware(
            labels={
                "host": from_header("X-User", allowed_values=("frank", "estelle"))
            }
        )
    ```
    """

    def inner(r: Request):
        v = r.headers.get(key, "")

        # if allowed_values was supplied, return a blank string if
        # the value of the header does match any of the values.
        if allowed_values is not None and v not in allowed_values:
            return ""

        return v

    return inner
