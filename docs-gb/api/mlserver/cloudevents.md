# Module `mlserver.cloudevents`


## Class `CloudEventsMiddleware`


**Description:**
Base class to implement middlewares.

### Method `request_middleware`


**Signature:** `request_middleware(self, request: mlserver.types.dataplane.InferenceRequest, model_settings: mlserver.settings.ModelSettings) -> mlserver.types.dataplane.InferenceRequest`


**Description:**
*No docstring available.*

### Method `response_middleware`


**Signature:** `response_middleware(self, response: mlserver.types.dataplane.InferenceResponse, model_settings: mlserver.settings.ModelSettings) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
*No docstring available.*

## Class `CloudEventsTypes`


**Description:**
Create a collection of name/value pairs.
Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.

## Function `get_namespace`


**Signature:** `get_namespace() -> Optional[str]`


**Description:**
*No docstring available.*
