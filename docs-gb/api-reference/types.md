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

**JSON Schema:**

```json
{
  "properties": {
    "error": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Error"
    }
  },
  "title": "InferenceErrorResponse",
  "type": "object"
}
```


### Class `InferenceRequest`

```python
class InferenceRequest
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    },
    "RequestInput": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "shape": {
          "items": {
            "type": "integer"
          },
          "title": "Shape",
          "type": "array"
        },
        "datatype": {
          "$ref": "#/$defs/Datatype"
        },
        "parameters": {
          "anyOf": [
            {
              "$ref": "#/$defs/Parameters"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "data": {
          "$ref": "#/$defs/TensorData"
        }
      },
      "required": [
        "name",
        "shape",
        "datatype",
        "data"
      ],
      "title": "RequestInput",
      "type": "object"
    },
    "RequestOutput": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "parameters": {
          "anyOf": [
            {
              "$ref": "#/$defs/Parameters"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "name"
      ],
      "title": "RequestOutput",
      "type": "object"
    },
    "TensorData": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {}
      ],
      "title": "TensorData"
    }
  },
  "properties": {
    "id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Id"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "inputs": {
      "items": {
        "$ref": "#/$defs/RequestInput"
      },
      "title": "Inputs",
      "type": "array"
    },
    "outputs": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/$defs/RequestOutput"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Outputs"
    }
  },
  "required": [
    "inputs"
  ],
  "title": "InferenceRequest",
  "type": "object"
}
```


### Class `InferenceResponse`

```python
class InferenceResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    },
    "ResponseOutput": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "shape": {
          "items": {
            "type": "integer"
          },
          "title": "Shape",
          "type": "array"
        },
        "datatype": {
          "$ref": "#/$defs/Datatype"
        },
        "parameters": {
          "anyOf": [
            {
              "$ref": "#/$defs/Parameters"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "data": {
          "$ref": "#/$defs/TensorData"
        }
      },
      "required": [
        "name",
        "shape",
        "datatype",
        "data"
      ],
      "title": "ResponseOutput",
      "type": "object"
    },
    "TensorData": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {}
      ],
      "title": "TensorData"
    }
  },
  "properties": {
    "model_name": {
      "title": "Model Name",
      "type": "string"
    },
    "model_version": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Model Version"
    },
    "id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Id"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "outputs": {
      "items": {
        "$ref": "#/$defs/ResponseOutput"
      },
      "title": "Outputs",
      "type": "array"
    }
  },
  "required": [
    "model_name",
    "outputs"
  ],
  "title": "InferenceResponse",
  "type": "object"
}
```


### Class `MetadataModelErrorResponse`

```python
class MetadataModelErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "properties": {
    "error": {
      "title": "Error",
      "type": "string"
    }
  },
  "required": [
    "error"
  ],
  "title": "MetadataModelErrorResponse",
  "type": "object"
}
```


### Class `MetadataModelResponse`

```python
class MetadataModelResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "MetadataTensor": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "datatype": {
          "$ref": "#/$defs/Datatype"
        },
        "shape": {
          "items": {
            "type": "integer"
          },
          "title": "Shape",
          "type": "array"
        },
        "parameters": {
          "anyOf": [
            {
              "$ref": "#/$defs/Parameters"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "name",
        "datatype",
        "shape"
      ],
      "title": "MetadataTensor",
      "type": "object"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "versions": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Versions"
    },
    "platform": {
      "title": "Platform",
      "type": "string"
    },
    "inputs": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/$defs/MetadataTensor"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Inputs"
    },
    "outputs": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/$defs/MetadataTensor"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Outputs"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "name",
    "platform"
  ],
  "title": "MetadataModelResponse",
  "type": "object"
}
```


### Class `MetadataServerErrorResponse`

```python
class MetadataServerErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "properties": {
    "error": {
      "title": "Error",
      "type": "string"
    }
  },
  "required": [
    "error"
  ],
  "title": "MetadataServerErrorResponse",
  "type": "object"
}
```


### Class `MetadataServerResponse`

```python
class MetadataServerResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "version": {
      "title": "Version",
      "type": "string"
    },
    "extensions": {
      "items": {
        "type": "string"
      },
      "title": "Extensions",
      "type": "array"
    }
  },
  "required": [
    "name",
    "version",
    "extensions"
  ],
  "title": "MetadataServerResponse",
  "type": "object"
}
```


### Class `MetadataTensor`

```python
class MetadataTensor
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "datatype": {
      "$ref": "#/$defs/Datatype"
    },
    "shape": {
      "items": {
        "type": "integer"
      },
      "title": "Shape",
      "type": "array"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "name",
    "datatype",
    "shape"
  ],
  "title": "MetadataTensor",
  "type": "object"
}
```


### Class `Parameters`

```python
class Parameters
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "additionalProperties": true,
  "properties": {
    "content_type": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Content Type"
    },
    "headers": {
      "anyOf": [
        {
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Headers"
    }
  },
  "title": "Parameters",
  "type": "object"
}
```


### Class `RepositoryIndexRequest`

```python
class RepositoryIndexRequest
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "properties": {
    "ready": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Ready"
    }
  },
  "title": "RepositoryIndexRequest",
  "type": "object"
}
```


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

**JSON Schema:**

```json
{
  "$defs": {
    "RepositoryIndexResponseItem": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "version": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Version"
        },
        "state": {
          "$ref": "#/$defs/State"
        },
        "reason": {
          "title": "Reason",
          "type": "string"
        }
      },
      "required": [
        "name",
        "state",
        "reason"
      ],
      "title": "RepositoryIndexResponseItem",
      "type": "object"
    },
    "State": {
      "enum": [
        "UNKNOWN",
        "READY",
        "UNAVAILABLE",
        "LOADING",
        "UNLOADING"
      ],
      "title": "State",
      "type": "string"
    }
  },
  "items": {
    "$ref": "#/$defs/RepositoryIndexResponseItem"
  },
  "title": "RepositoryIndexResponse",
  "type": "array"
}
```


### Class `RepositoryIndexResponseItem`

```python
class RepositoryIndexResponseItem
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "State": {
      "enum": [
        "UNKNOWN",
        "READY",
        "UNAVAILABLE",
        "LOADING",
        "UNLOADING"
      ],
      "title": "State",
      "type": "string"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "version": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Version"
    },
    "state": {
      "$ref": "#/$defs/State"
    },
    "reason": {
      "title": "Reason",
      "type": "string"
    }
  },
  "required": [
    "name",
    "state",
    "reason"
  ],
  "title": "RepositoryIndexResponseItem",
  "type": "object"
}
```


### Class `RepositoryLoadErrorResponse`

```python
class RepositoryLoadErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "properties": {
    "error": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Error"
    }
  },
  "title": "RepositoryLoadErrorResponse",
  "type": "object"
}
```


### Class `RepositoryUnloadErrorResponse`

```python
class RepositoryUnloadErrorResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "properties": {
    "error": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Error"
    }
  },
  "title": "RepositoryUnloadErrorResponse",
  "type": "object"
}
```


### Class `RequestInput`

```python
class RequestInput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    },
    "TensorData": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {}
      ],
      "title": "TensorData"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "shape": {
      "items": {
        "type": "integer"
      },
      "title": "Shape",
      "type": "array"
    },
    "datatype": {
      "$ref": "#/$defs/Datatype"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "data": {
      "$ref": "#/$defs/TensorData"
    }
  },
  "required": [
    "name",
    "shape",
    "datatype",
    "data"
  ],
  "title": "RequestInput",
  "type": "object"
}
```


### Class `RequestOutput`

```python
class RequestOutput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "name"
  ],
  "title": "RequestOutput",
  "type": "object"
}
```


### Class `ResponseOutput`

```python
class ResponseOutput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

**JSON Schema:**

```json
{
  "$defs": {
    "Datatype": {
      "enum": [
        "BOOL",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "FP16",
        "FP32",
        "FP64",
        "BYTES"
      ],
      "title": "Datatype",
      "type": "string"
    },
    "Parameters": {
      "additionalProperties": true,
      "properties": {
        "content_type": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Content Type"
        },
        "headers": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Headers"
        }
      },
      "title": "Parameters",
      "type": "object"
    },
    "TensorData": {
      "anyOf": [
        {
          "items": {},
          "type": "array"
        },
        {}
      ],
      "title": "TensorData"
    }
  },
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "shape": {
      "items": {
        "type": "integer"
      },
      "title": "Shape",
      "type": "array"
    },
    "datatype": {
      "$ref": "#/$defs/Datatype"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/Parameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "data": {
      "$ref": "#/$defs/TensorData"
    }
  },
  "required": [
    "name",
    "shape",
    "datatype",
    "data"
  ],
  "title": "ResponseOutput",
  "type": "object"
}
```


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

**JSON Schema:**

```json
{
  "anyOf": [
    {
      "items": {},
      "type": "array"
    },
    {}
  ],
  "title": "TensorData"
}
```

