# Module `mlserver.rest.utils`


## Function `matches`


**Signature:** `matches(route: fastapi.routing.APIRoute, custom_handler: mlserver.handlers.custom.CustomHandler, handler_method: Callable) -> bool`


**Description:**
*No docstring available.*

## Function `to_scope`


**Signature:** `to_scope(custom_handler: mlserver.handlers.custom.CustomHandler) -> collections.abc.MutableMapping[str, typing.Any]`


**Description:**
*No docstring available.*

## Function `to_status_code`


**Signature:** `to_status_code(flag: bool, error_code: int = 400) -> int`


**Description:**
Convert a boolean flag into a HTTP status code.
