# Settings

### *pydantic settings* mlserver.settings.Settings

Bases: `BaseSettings`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "Settings",
   "type": "object",
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
         "default": "/Users/paul.bridi/Projects/MLServer/docs-gb/.envs",
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
         "default": "/Users/paul.bridi/Projects/MLServer/docs-gb/.metrics",
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
   }
}
```

</details></p>
* **Fields:**
  - [`cache_enabled (bool)`](#mlserver.settings.Settings.cache_enabled)
  - [`cache_size (int)`](#mlserver.settings.Settings.cache_size)
  - [`cors_settings (mlserver.settings.CORSSettings | None)`](#mlserver.settings.Settings.cors_settings)
  - [`debug (bool)`](#mlserver.settings.Settings.debug)
  - [`environments_dir (str)`](#mlserver.settings.Settings.environments_dir)
  - [`extensions (List[str])`](#mlserver.settings.Settings.extensions)
  - [`grpc_max_message_length (int | None)`](#mlserver.settings.Settings.grpc_max_message_length)
  - [`grpc_port (int)`](#mlserver.settings.Settings.grpc_port)
  - [`gzip_enabled (bool)`](#mlserver.settings.Settings.gzip_enabled)
  - [`host (str)`](#mlserver.settings.Settings.host)
  - [`http_port (int)`](#mlserver.settings.Settings.http_port)
  - [`kafka_enabled (bool)`](#mlserver.settings.Settings.kafka_enabled)
  - [`kafka_servers (str)`](#mlserver.settings.Settings.kafka_servers)
  - [`kafka_topic_input (str)`](#mlserver.settings.Settings.kafka_topic_input)
  - [`kafka_topic_output (str)`](#mlserver.settings.Settings.kafka_topic_output)
  - [`load_models_at_startup (bool)`](#mlserver.settings.Settings.load_models_at_startup)
  - [`logging_settings (str | Dict | None)`](#mlserver.settings.Settings.logging_settings)
  - [`metrics_dir (str)`](#mlserver.settings.Settings.metrics_dir)
  - [`metrics_endpoint (str | None)`](#mlserver.settings.Settings.metrics_endpoint)
  - [`metrics_port (int)`](#mlserver.settings.Settings.metrics_port)
  - [`metrics_rest_server_prefix (str)`](#mlserver.settings.Settings.metrics_rest_server_prefix)
  - [`model_repository_implementation (pydantic.types.ImportString | None)`](#mlserver.settings.Settings.model_repository_implementation)
  - [`model_repository_implementation_args (dict)`](#mlserver.settings.Settings.model_repository_implementation_args)
  - [`model_repository_root (str)`](#mlserver.settings.Settings.model_repository_root)
  - [`parallel_workers (int)`](#mlserver.settings.Settings.parallel_workers)
  - [`parallel_workers_timeout (int)`](#mlserver.settings.Settings.parallel_workers_timeout)
  - [`root_path (str)`](#mlserver.settings.Settings.root_path)
  - [`server_name (str)`](#mlserver.settings.Settings.server_name)
  - [`server_version (str)`](#mlserver.settings.Settings.server_version)
  - [`tracing_server (str | None)`](#mlserver.settings.Settings.tracing_server)
  - [`use_structured_logging (bool)`](#mlserver.settings.Settings.use_structured_logging)

#### *field* cache_enabled *: bool* *= False*

Enable caching for the model predictions.

#### *field* cache_size *: int* *= 100*

Cache size to be used if caching is enabled.

#### *field* cors_settings *: CORSSettings | None* *= None*

#### *field* debug *: bool* *= True*

#### *field* environments_dir *: str* *= '/Users/paul.bridi/Projects/MLServer/docs-gb/.envs'*

Directory used to store custom environments.
By default, the .envs folder of the current working directory will be
used.

#### *field* extensions *: List[str]* *= []*

Server extensions loaded.

#### *field* grpc_max_message_length *: int | None* *= None*

Maximum length (i.e. size) of gRPC payloads.

#### *field* grpc_port *: int* *= 8081*

Port where to listen for gRPC connections.

#### *field* gzip_enabled *: bool* *= True*

Enable GZipMiddleware.

#### *field* host *: str* *= '0.0.0.0'*

Host where to listen for connections.

#### *field* http_port *: int* *= 8080*

Port where to listen for HTTP / REST connections.

#### *field* kafka_enabled *: bool* *= False*

#### *field* kafka_servers *: str* *= 'localhost:9092'*

#### *field* kafka_topic_input *: str* *= 'mlserver-input'*

#### *field* kafka_topic_output *: str* *= 'mlserver-output'*

#### *field* load_models_at_startup *: bool* *= True*

Flag to load all available models automatically at startup.

#### *field* logging_settings *: str | Dict | None* *= None*

Path to logging config file or dictionary configuration.

#### *field* metrics_dir *: str* *= '/Users/paul.bridi/Projects/MLServer/docs-gb/.metrics'*

Directory used to share metrics across parallel workers.
Equivalent to the PROMETHEUS_MULTIPROC_DIR env var in
prometheus-client.
Note that this won’t be used if the parallel_workers flag is disabled.
By default, the .metrics folder of the current working directory will be
used.

#### *field* metrics_endpoint *: str | None* *= '/metrics'*

Endpoint used to expose Prometheus metrics. Alternatively, can be set to
None to disable it.

#### *field* metrics_port *: int* *= 8082*

Port used to expose metrics endpoint.

#### *field* metrics_rest_server_prefix *: str* *= 'rest_server'*

Metrics rest server string prefix to be exported.

#### *field* model_repository_implementation *: ImportString | None* *= None*

*Python path* to the inference runtime to model repository (e.g.
`mlserver.repository.repository.SchemalessModelRepository`).

#### *field* model_repository_implementation_args *: dict* *= {}*

Extra parameters for model repository.

#### *field* model_repository_root *: str* *= '.'*

Root of the model repository, where we will search for models.

#### *field* parallel_workers *: int* *= 1*

When parallel inference is enabled, number of workers to run inference
across.

#### *field* parallel_workers_timeout *: int* *= 5*

Grace timeout to wait until the workers shut down when stopping MLServer.

#### *field* root_path *: str* *= ''*

Set the ASGI root_path for applications submounted below a given URL path.

#### *field* server_name *: str* *= 'mlserver'*

Name of the server.

#### *field* server_version *: str* *= '1.7.0.dev0'*

Version of the server.

#### *field* tracing_server *: str | None* *= None*

Server name used to export OpenTelemetry tracing to collector service.

#### *field* use_structured_logging *: bool* *= False*

Use JSON-formatted structured logging instead of default format.

#### model_post_init(context,)

This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that’s what pydantic-core passes when calling it.

* **Parameters:**
  * **self** (*BaseModel*) – The BaseModel instance.
  * **context** (*Any*) – The context.
* **Return type:**
  None
