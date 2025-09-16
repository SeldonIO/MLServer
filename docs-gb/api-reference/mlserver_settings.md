# MLServer Settings

## Module `mlserver.settings`

### Class `BaseSettings`

```python
class BaseSettings
```



**JSON Schema:**

```json
{
  "additionalProperties": false,
  "properties": {},
  "title": "BaseSettings",
  "type": "object"
}
```


### Class `CORSSettings`

```python
class CORSSettings
```



**JSON Schema:**

```json
{
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
```


### Class `Settings`

```python
class Settings
```



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


### Class `ModelParameters`

```python
class ModelParameters
```

Parameters that apply only to a particular instance of a model.
This can include things like model weights, or arbitrary ``extra``
parameters particular to the underlying inference runtime.
The main difference with respect to ``ModelSettings`` is that parameters
can change on each instance (e.g. each version) of the model.

**JSON Schema:**

```json
{
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
}
```


### Class `ModelSettings`

```python
class ModelSettings
```



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

