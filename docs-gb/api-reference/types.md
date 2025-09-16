# Types

## Module `mlserver.types`

### Class `Datatype`

```python
class Datatype
```

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

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


### Class `InferenceErrorResponse`

```python
class InferenceErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `InferenceRequest`

```python
class InferenceRequest
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `InferenceResponse`

```python
class InferenceResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `MetadataModelErrorResponse`

```python
class MetadataModelErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `MetadataModelResponse`

```python
class MetadataModelResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `MetadataServerErrorResponse`

```python
class MetadataServerErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `MetadataServerResponse`

```python
class MetadataServerResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `MetadataTensor`

```python
class MetadataTensor
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `Parameters`

```python
class Parameters
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RepositoryIndexRequest`

```python
class RepositoryIndexRequest
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RepositoryIndexResponse`

```python
class RepositoryIndexResponse
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/#rootmodel-and-custom-root-types

A Pydantic `BaseModel` for the root object of the model.

Attributes:
    root: The root object of the model.
    __pydantic_root_model__: Whether the model is a RootModel.
    __pydantic_private__: Private fields in the model.
    __pydantic_extra__: Extra fields in the model.


### Class `RepositoryIndexResponseItem`

```python
class RepositoryIndexResponseItem
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RepositoryLoadErrorResponse`

```python
class RepositoryLoadErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RepositoryUnloadErrorResponse`

```python
class RepositoryUnloadErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RequestInput`

```python
class RequestInput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RequestOutput`

```python
class RequestOutput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `ResponseOutput`

```python
class ResponseOutput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `State`

```python
class State
```

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access::

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


### Class `TensorData`

```python
class TensorData
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/#rootmodel-and-custom-root-types

A Pydantic `BaseModel` for the root object of the model.

Attributes:
    root: The root object of the model.
    __pydantic_root_model__: Whether the model is a RootModel.
    __pydantic_private__: Private fields in the model.
    __pydantic_extra__: Extra fields in the model.

