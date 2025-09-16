# Module `mlserver.kafka.server`


## Class `KafkaMethodTypes`


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

## Class `KafkaServer`


**Description:**
*No docstring available.*

### Method `add_custom_handlers`


**Signature:** `add_custom_handlers(self, model: mlserver.model.MLModel)`


**Description:**
*No docstring available.*

### Method `delete_custom_handlers`


**Signature:** `delete_custom_handlers(self, model: mlserver.model.MLModel)`


**Description:**
*No docstring available.*

### Method `start`


**Signature:** `start(self)`


**Description:**
*No docstring available.*

### Method `stop`


**Signature:** `stop(self, sig: Optional[int] = None)`


**Description:**
*No docstring available.*
