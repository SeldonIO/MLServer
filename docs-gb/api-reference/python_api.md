# Python API

## Module `mlserver`

### Class `MLModel`

```python
class MLModel
```

Abstract inference runtime which exposes the main interface to interact
with ML models.


### Class `MLServer`

```python
class MLServer
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


### Class `Settings`

```python
class Settings
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
    "CORSSettings": {
      "properties": {
        "allow_origins": {
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
          "default": [],
          "title": "Allow Origins"
        },
        "allow_origin_regex": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Allow Origin Regex"
        },
        "allow_credentials": {
          "anyOf": [
            {
              "type": "boolean"
            },
            {
              "type": "null"
            }
          ],
          "default": false,
          "title": "Allow Credentials"
        },
        "allow_methods": {
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
          "default": [
            "GET"
          ],
          "title": "Allow Methods"
        },
        "allow_headers": {
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
          "default": [],
          "title": "Allow Headers"
        },
        "expose_headers": {
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
          "default": [],
          "title": "Expose Headers"
        },
        "max_age": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": 600,
          "title": "Max Age"
        }
      },
      "title": "CORSSettings",
      "type": "object"
    }
  },
  "properties": {
    "debug": {
      "default": true,
      "title": "Debug",
      "type": "boolean"
    },
    "parallel_workers": {
      "default": 1,
      "title": "Parallel Workers",
      "type": "integer"
    },
    "parallel_workers_timeout": {
      "default": 5,
      "title": "Parallel Workers Timeout",
      "type": "integer"
    },
    "environments_dir": {
      "default": "/Users/paul.bridi/Projects/MLServer/.envs",
      "title": "Environments Dir",
      "type": "string"
    },
    "model_repository_implementation": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Model Repository Implementation"
    },
    "model_repository_root": {
      "default": ".",
      "title": "Model Repository Root",
      "type": "string"
    },
    "model_repository_implementation_args": {
      "default": {},
      "title": "Model Repository Implementation Args",
      "type": "object"
    },
    "load_models_at_startup": {
      "default": true,
      "title": "Load Models At Startup",
      "type": "boolean"
    },
    "server_name": {
      "default": "mlserver",
      "title": "Server Name",
      "type": "string"
    },
    "server_version": {
      "default": "1.7.0.dev0",
      "title": "Server Version",
      "type": "string"
    },
    "extensions": {
      "default": [],
      "items": {
        "type": "string"
      },
      "title": "Extensions",
      "type": "array"
    },
    "host": {
      "default": "0.0.0.0",
      "title": "Host",
      "type": "string"
    },
    "http_port": {
      "default": 8080,
      "title": "Http Port",
      "type": "integer"
    },
    "root_path": {
      "default": "",
      "title": "Root Path",
      "type": "string"
    },
    "grpc_port": {
      "default": 8081,
      "title": "Grpc Port",
      "type": "integer"
    },
    "grpc_max_message_length": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Grpc Max Message Length"
    },
    "cors_settings": {
      "anyOf": [
        {
          "$ref": "#/$defs/CORSSettings"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "metrics_endpoint": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "/metrics",
      "title": "Metrics Endpoint"
    },
    "metrics_port": {
      "default": 8082,
      "title": "Metrics Port",
      "type": "integer"
    },
    "metrics_rest_server_prefix": {
      "default": "rest_server",
      "title": "Metrics Rest Server Prefix",
      "type": "string"
    },
    "metrics_dir": {
      "default": "/Users/paul.bridi/Projects/MLServer/.metrics",
      "title": "Metrics Dir",
      "type": "string"
    },
    "use_structured_logging": {
      "default": false,
      "title": "Use Structured Logging",
      "type": "boolean"
    },
    "logging_settings": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "object"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Logging Settings"
    },
    "kafka_enabled": {
      "default": false,
      "title": "Kafka Enabled",
      "type": "boolean"
    },
    "kafka_servers": {
      "default": "localhost:9092",
      "title": "Kafka Servers",
      "type": "string"
    },
    "kafka_topic_input": {
      "default": "mlserver-input",
      "title": "Kafka Topic Input",
      "type": "string"
    },
    "kafka_topic_output": {
      "default": "mlserver-output",
      "title": "Kafka Topic Output",
      "type": "string"
    },
    "tracing_server": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Tracing Server"
    },
    "cache_enabled": {
      "default": false,
      "title": "Cache Enabled",
      "type": "boolean"
    },
    "cache_size": {
      "default": 100,
      "title": "Cache Size",
      "type": "integer"
    },
    "gzip_enabled": {
      "default": true,
      "title": "Gzip Enabled",
      "type": "boolean"
    }
  },
  "title": "Settings",
  "type": "object"
}
```


### Function `log`

```python
log(**metrics)
```

Logs a new set of metric values.
Each kwarg of this method will be treated as a separate metric / value
pair.
If any of the metrics does not exist, a new one will be created with a
default description.


### Function `register`

```python
register(name: str, description: str) -> prometheus_client.metrics.Histogram
```

Registers a new metric with its description.
If the metric already exists, it will just return the existing one.

