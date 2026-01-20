# Module `mlserver.rest.requests`


## Class `Request`


**Description:**
Custom request class which uses `orjson` if present.
Otherwise, it falls back to the standard FastAPI request.

### Method `body`


**Signature:** `body(self) -> bytes`


**Description:**
*No docstring available.*

### Method `close`


**Signature:** `close(self) -> 'None'`


**Description:**
*No docstring available.*

### Method `form`


**Signature:** `form(self, *, max_files: 'int | float' = 1000, max_fields: 'int | float' = 1000, max_part_size: 'int' = 1048576) -> 'AwaitableOrContextManager[FormData]'`


**Description:**
*No docstring available.*

### Method `get`


**Signature:** `get(self, key, default=None)`


**Description:**
D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.

### Method `is_disconnected`


**Signature:** `is_disconnected(self) -> 'bool'`


**Description:**
*No docstring available.*

### Method `items`


**Signature:** `items(self)`


**Description:**
D.items() -> a set-like object providing a view on D's items

### Method `json`


**Signature:** `json(self) -> Any`


**Description:**
*No docstring available.*

### Method `keys`


**Signature:** `keys(self)`


**Description:**
D.keys() -> a set-like object providing a view on D's keys

### Method `send_push_promise`


**Signature:** `send_push_promise(self, path: 'str') -> 'None'`


**Description:**
*No docstring available.*

### Method `stream`


**Signature:** `stream(self) -> 'AsyncGenerator[bytes, None]'`


**Description:**
*No docstring available.*

### Method `url_for`


**Signature:** `url_for(self, name: 'str', /, **path_params: 'Any') -> 'URL'`


**Description:**
*No docstring available.*

### Method `values`


**Signature:** `values(self)`


**Description:**
D.values() -> an object providing a view on D's values
