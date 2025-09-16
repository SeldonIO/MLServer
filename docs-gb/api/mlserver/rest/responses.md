# Module `mlserver.rest.responses`


## Class `Response`


**Description:**
Custom Response that will use the encode_to_json_bytes function to
encode given content to json based on library availability.
See mlserver/codecs/utils.py for more details

### Method `delete_cookie`


**Signature:** `delete_cookie(self, key: 'str', path: 'str' = '/', domain: 'str | None' = None, secure: 'bool' = False, httponly: 'bool' = False, samesite: "Literal['lax', 'strict', 'none'] | None" = 'lax') -> 'None'`


**Description:**
*No docstring available.*

### Method `init_headers`


**Signature:** `init_headers(self, headers: 'Mapping[str, str] | None' = None) -> 'None'`


**Description:**
*No docstring available.*

### Method `render`


**Signature:** `render(self, content: Any) -> bytes`


**Description:**
*No docstring available.*

### Method `set_cookie`


**Signature:** `set_cookie(self, key: 'str', value: 'str' = '', max_age: 'int | None' = None, expires: 'datetime | str | int | None' = None, path: 'str | None' = '/', domain: 'str | None' = None, secure: 'bool' = False, httponly: 'bool' = False, samesite: "Literal['lax', 'strict', 'none'] | None" = 'lax', partitioned: 'bool' = False) -> 'None'`


**Description:**
*No docstring available.*

## Class `ServerSentEvent`


**Description:**
*No docstring available.*

### Method `encode`


**Signature:** `encode(self) -> bytes`


**Description:**
*No docstring available.*
