# Module `mlserver.rest.app`


## Class `APIRoute`


**Description:**
Custom route to use our own Request handler.

### Method `get_route_handler`


**Signature:** `get_route_handler(self) -> Callable`


**Description:**
*No docstring available.*

### Method `handle`


**Signature:** `handle(self, scope: 'Scope', receive: 'Receive', send: 'Send') -> 'None'`


**Description:**
*No docstring available.*

### Method `matches`


**Signature:** `matches(self, scope: collections.abc.MutableMapping[str, typing.Any]) -> Tuple[starlette.routing.Match, collections.abc.MutableMapping[str, Any]]`


**Description:**
*No docstring available.*

### Method `url_path_for`


**Signature:** `url_path_for(self, name: 'str', /, **path_params: 'Any') -> 'URLPath'`


**Description:**
*No docstring available.*

## Function `create_app`


**Signature:** `create_app(settings: mlserver.settings.Settings, data_plane: mlserver.handlers.dataplane.DataPlane, model_repository_handlers: mlserver.handlers.model_repository.ModelRepositoryHandlers) -> fastapi.applications.FastAPI`


**Description:**
*No docstring available.*
