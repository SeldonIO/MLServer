<a id="settings"></a>

# Settings

<a id="mlserver.settings.Settings"></a>

### *pydantic settings* mlserver.settings.Settings

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

<a id="mlserver.settings.Settings.cache_enabled"></a>

#### *field* cache_enabled *: bool* *= False*

Enable caching for the model predictions.

<a id="mlserver.settings.Settings.cache_size"></a>

#### *field* cache_size *: int* *= 100*

Cache size to be used if caching is enabled.

<a id="mlserver.settings.Settings.cors_settings"></a>

#### *field* cors_settings *: CORSSettings | None* *= None*

<a id="mlserver.settings.Settings.debug"></a>

#### *field* debug *: bool* *= True*

<a id="mlserver.settings.Settings.environments_dir"></a>

#### *field* environments_dir *: str* *= '/Users/paul.bridi/Projects/MLServer/docs-gb/.envs'*

Directory used to store custom environments.
By default, the .envs folder of the current working directory will be
used.

<a id="mlserver.settings.Settings.extensions"></a>

#### *field* extensions *: List[str]* *= []*

Server extensions loaded.

<a id="mlserver.settings.Settings.grpc_max_message_length"></a>

#### *field* grpc_max_message_length *: int | None* *= None*

Maximum length (i.e. size) of gRPC payloads.

<a id="mlserver.settings.Settings.grpc_port"></a>

#### *field* grpc_port *: int* *= 8081*

Port where to listen for gRPC connections.

<a id="mlserver.settings.Settings.gzip_enabled"></a>

#### *field* gzip_enabled *: bool* *= True*

Enable GZipMiddleware.

<a id="mlserver.settings.Settings.host"></a>

#### *field* host *: str* *= '0.0.0.0'*

Host where to listen for connections.

<a id="mlserver.settings.Settings.http_port"></a>

#### *field* http_port *: int* *= 8080*

Port where to listen for HTTP / REST connections.

<a id="mlserver.settings.Settings.kafka_enabled"></a>

#### *field* kafka_enabled *: bool* *= False*

<a id="mlserver.settings.Settings.kafka_servers"></a>

#### *field* kafka_servers *: str* *= 'localhost:9092'*

<a id="mlserver.settings.Settings.kafka_topic_input"></a>

#### *field* kafka_topic_input *: str* *= 'mlserver-input'*

<a id="mlserver.settings.Settings.kafka_topic_output"></a>

#### *field* kafka_topic_output *: str* *= 'mlserver-output'*

<a id="mlserver.settings.Settings.load_models_at_startup"></a>

#### *field* load_models_at_startup *: bool* *= True*

Flag to load all available models automatically at startup.

<a id="mlserver.settings.Settings.logging_settings"></a>

#### *field* logging_settings *: str | Dict | None* *= None*

Path to logging config file or dictionary configuration.

<a id="mlserver.settings.Settings.metrics_dir"></a>

#### *field* metrics_dir *: str* *= '/Users/paul.bridi/Projects/MLServer/docs-gb/.metrics'*

Directory used to share metrics across parallel workers.
Equivalent to the PROMETHEUS_MULTIPROC_DIR env var in
prometheus-client.
Note that this won’t be used if the parallel_workers flag is disabled.
By default, the .metrics folder of the current working directory will be
used.

<a id="mlserver.settings.Settings.metrics_endpoint"></a>

#### *field* metrics_endpoint *: str | None* *= '/metrics'*

Endpoint used to expose Prometheus metrics. Alternatively, can be set to
None to disable it.

<a id="mlserver.settings.Settings.metrics_port"></a>

#### *field* metrics_port *: int* *= 8082*

Port used to expose metrics endpoint.

<a id="mlserver.settings.Settings.metrics_rest_server_prefix"></a>

#### *field* metrics_rest_server_prefix *: str* *= 'rest_server'*

Metrics rest server string prefix to be exported.

<a id="mlserver.settings.Settings.model_repository_implementation"></a>

#### *field* model_repository_implementation *: ImportString | None* *= None*

*Python path* to the inference runtime to model repository (e.g.
`mlserver.repository.repository.SchemalessModelRepository`).

<a id="mlserver.settings.Settings.model_repository_implementation_args"></a>

#### *field* model_repository_implementation_args *: dict* *= {}*

Extra parameters for model repository.

<a id="mlserver.settings.Settings.model_repository_root"></a>

#### *field* model_repository_root *: str* *= '.'*

Root of the model repository, where we will search for models.

<a id="mlserver.settings.Settings.parallel_workers"></a>

#### *field* parallel_workers *: int* *= 1*

When parallel inference is enabled, number of workers to run inference
across.

<a id="mlserver.settings.Settings.parallel_workers_timeout"></a>

#### *field* parallel_workers_timeout *: int* *= 5*

Grace timeout to wait until the workers shut down when stopping MLServer.

<a id="mlserver.settings.Settings.root_path"></a>

#### *field* root_path *: str* *= ''*

Set the ASGI root_path for applications submounted below a given URL path.

<a id="mlserver.settings.Settings.server_name"></a>

#### *field* server_name *: str* *= 'mlserver'*

Name of the server.

<a id="mlserver.settings.Settings.server_version"></a>

#### *field* server_version *: str* *= '1.7.0.dev0'*

Version of the server.

<a id="mlserver.settings.Settings.tracing_server"></a>

#### *field* tracing_server *: str | None* *= None*

Server name used to export OpenTelemetry tracing to collector service.

<a id="mlserver.settings.Settings.use_structured_logging"></a>

#### *field* use_structured_logging *: bool* *= False*

Use JSON-formatted structured logging instead of default format.

<a id="mlserver.settings.Settings.model_post_init"></a>

#### model_post_init(context,)

This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that’s what pydantic-core passes when calling it.

* **Parameters:**
  * **self** (*BaseModel*) – The BaseModel instance.
  * **context** (*Any*) – The context.
* **Return type:**
  None
