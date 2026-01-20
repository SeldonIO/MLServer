# Module `mlserver.utils`


## Function `extract_headers`


**Signature:** `extract_headers(inference_response: mlserver.types.dataplane.InferenceResponse) -> Optional[Dict[str, str]]`


**Description:**
*No docstring available.*

## Function `generate_uuid`


**Signature:** `generate_uuid() -> str`


**Description:**
*No docstring available.*

## Function `get_model_uri`


**Signature:** `get_model_uri(settings: mlserver.settings.ModelSettings, wellknown_filenames: List[str] = []) -> str`


**Description:**
*No docstring available.*

## Function `get_wrapped_method`


**Signature:** `get_wrapped_method(f: Callable) -> Callable`


**Description:**
*No docstring available.*

## Function `insert_headers`


**Signature:** `insert_headers(inference_request: mlserver.types.dataplane.InferenceRequest, headers: Dict[str, str]) -> mlserver.types.dataplane.InferenceRequest`


**Description:**
*No docstring available.*

## Function `install_uvloop_event_loop`


**Signature:** `install_uvloop_event_loop()`


**Description:**
*No docstring available.*

## Function `schedule_with_callback`


**Signature:** `schedule_with_callback(coro, cb) -> _asyncio.Task`


**Description:**
*No docstring available.*

## Function `to_absolute_path`


**Signature:** `to_absolute_path(model_settings: mlserver.settings.ModelSettings, uri: str) -> str`


**Description:**
*No docstring available.*
