# Module `mlserver.rest.logging`


## Class `HealthEndpointFilter`


**Description:**
Filter to avoid logging health endpoints.
From:
    https://github.com/encode/starlette/issues/864#issuecomment-653076434

### Method `filter`


**Signature:** `filter(self, record: logging.LogRecord) -> bool`


**Description:**
Determine if the specified record is to be logged.
Returns True if the record should be logged, or False otherwise.
If deemed appropriate, the record may be modified in-place.

## Function `disable_health_access_logs`


**Signature:** `disable_health_access_logs() -> None`


**Description:**
*No docstring available.*
