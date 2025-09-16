# Model Settings

## Module `mlserver.model`

### Class `Any`

```python
class Any
```

Special type indicating an unconstrained type.

- Any is compatible with every type.
- Any assumed to have all methods.
- All values assumed to be instances of Any.

Note that all the above statements are true from the point of view of
static type checkers. At runtime, Any should not be used with instance
checks.


### Class `CodecNotFound`

```python
class CodecNotFound
```

Common base class for all non-exit exceptions.


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


### Class `MLModel`

```python
class MLModel
```

Abstract inference runtime which exposes the main interface to interact
with ML models.


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


### Class `ModelSettings`

```python
class ModelSettings
```

Base class for settings, allowing values to be overridden by environment variables.

This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

Args:
    _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
        Defaults to `None`.
    _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
        Defaults to `False`.
    _env_prefix: Prefix for all environment variables. Defaults to `None`.
    _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
        means that the value from `model_config['env_file']` should be used. You can also pass
        `None` to indicate that environment variables should not be loaded from an env file.
    _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
    _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
    _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
    _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
        into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
    _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
    _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
        Otherwse, defaults to sys.argv[0].
    _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
        If set to `True`, defaults to sys.argv[1:].
    _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
    _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
        `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
        _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
    _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
    _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
    _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
    _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
        Defaults to `False`.
    _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
        Defaults to `True`.
    _cli_prefix: The root parser command line arguments prefix. Defaults to "".
    _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
    _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
        (e.g. --flag, --no-flag). Defaults to `False`.
    _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
    _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.

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
    "ModelParameters": {
      "additionalProperties": true,
      "description": "Parameters that apply only to a particular instance of a model.\nThis can include things like model weights, or arbitrary ``extra``\nparameters particular to the underlying inference runtime.\nThe main difference with respect to ``ModelSettings`` is that parameters\ncan change on each instance (e.g. each version) of the model.",
      "properties": {
        "uri": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Uri"
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
        "environment_path": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Environment Path"
        },
        "environment_tarball": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Environment Tarball"
        },
        "inference_pool_gid": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Inference Pool Gid"
        },
        "autogenerate_inference_pool_gid": {
          "default": false,
          "title": "Autogenerate Inference Pool Gid",
          "type": "boolean"
        },
        "format": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Format"
        },
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
        "extra": {
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": {},
          "title": "Extra"
        }
      },
      "title": "ModelParameters",
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
    "implementation": {
      "title": "Implementation",
      "type": "string"
    },
    "name": {
      "default": "",
      "title": "Name",
      "type": "string"
    },
    "platform": {
      "default": "",
      "title": "Platform",
      "type": "string"
    },
    "versions": {
      "default": [],
      "items": {
        "type": "string"
      },
      "title": "Versions",
      "type": "array"
    },
    "inputs": {
      "default": [],
      "items": {
        "$ref": "#/$defs/MetadataTensor"
      },
      "title": "Inputs",
      "type": "array"
    },
    "outputs": {
      "default": [],
      "items": {
        "$ref": "#/$defs/MetadataTensor"
      },
      "title": "Outputs",
      "type": "array"
    },
    "parallel_workers": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "deprecated": true,
      "description": "Use the `parallel_workers` field the server wide settings instead.",
      "title": "Parallel Workers"
    },
    "warm_workers": {
      "default": false,
      "deprecated": true,
      "description": "Inference workers will now always be `warmed up` at start time.",
      "title": "Warm Workers",
      "type": "boolean"
    },
    "max_batch_size": {
      "default": 0,
      "title": "Max Batch Size",
      "type": "integer"
    },
    "max_batch_time": {
      "default": 0.0,
      "title": "Max Batch Time",
      "type": "number"
    },
    "parameters": {
      "anyOf": [
        {
          "$ref": "#/$defs/ModelParameters"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "cache_enabled": {
      "default": false,
      "title": "Cache Enabled",
      "type": "boolean"
    }
  },
  "required": [
    "implementation"
  ],
  "title": "ModelSettings",
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


### Function `decode_inference_request`

```python
decode_inference_request(inference_request: mlserver.types.dataplane.InferenceRequest, model_settings: Optional[mlserver.settings.ModelSettings] = None, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```




### Function `decode_request_input`

```python
decode_request_input(request_input: mlserver.types.dataplane.RequestInput, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```




### Function `encode_inference_response`

```python
encode_inference_response(payload: Any, model_settings: mlserver.settings.ModelSettings) -> Optional[mlserver.types.dataplane.InferenceResponse]
```




### Function `encode_response_output`

```python
encode_response_output(payload: Any, request_output: mlserver.types.dataplane.RequestOutput, metadata_outputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[mlserver.types.dataplane.ResponseOutput]
```




### Function `get_decoded`

```python
get_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```




### Function `has_decoded`

```python
has_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> bool
```



