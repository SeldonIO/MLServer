# Settings {#settings}### *pydantic settings* mlserver.settings.Settings {#mlserver.settings.Settings}
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
#### *field* cache_enabled *: bool* *= False* {#mlserver.settings.Settings.cache_enabled}
Enable caching for the model predictions.
#### *field* cache_size *: int* *= 100* {#mlserver.settings.Settings.cache_size}
Cache size to be used if caching is enabled.
#### *field* cors_settings *: CORSSettings | None* *= None* {#mlserver.settings.Settings.cors_settings}#### *field* debug *: bool* *= True* {#mlserver.settings.Settings.debug}#### *field* environments_dir *: str* *= '/Users/paul.bridi/Projects/MLServer/docs-gb/.envs'* {#mlserver.settings.Settings.environments_dir}
Directory used to store custom environments.
By default, the .envs folder of the current working directory will be
used.
#### *field* extensions *: List[str]* *= []* {#mlserver.settings.Settings.extensions}
Server extensions loaded.
#### *field* grpc_max_message_length *: int | None* *= None* {#mlserver.settings.Settings.grpc_max_message_length}
Maximum length (i.e. size) of gRPC payloads.
#### *field* grpc_port *: int* *= 8081* {#mlserver.settings.Settings.grpc_port}
Port where to listen for gRPC connections.
#### *field* gzip_enabled *: bool* *= True* {#mlserver.settings.Settings.gzip_enabled}
Enable GZipMiddleware.
#### *field* host *: str* *= '0.0.0.0'* {#mlserver.settings.Settings.host}
Host where to listen for connections.
#### *field* http_port *: int* *= 8080* {#mlserver.settings.Settings.http_port}
Port where to listen for HTTP / REST connections.
#### *field* kafka_enabled *: bool* *= False* {#mlserver.settings.Settings.kafka_enabled}#### *field* kafka_servers *: str* *= 'localhost:9092'* {#mlserver.settings.Settings.kafka_servers}#### *field* kafka_topic_input *: str* *= 'mlserver-input'* {#mlserver.settings.Settings.kafka_topic_input}#### *field* kafka_topic_output *: str* *= 'mlserver-output'* {#mlserver.settings.Settings.kafka_topic_output}#### *field* load_models_at_startup *: bool* *= True* {#mlserver.settings.Settings.load_models_at_startup}
Flag to load all available models automatically at startup.
#### *field* logging_settings *: str | Dict | None* *= None* {#mlserver.settings.Settings.logging_settings}
Path to logging config file or dictionary configuration.
#### *field* metrics_dir *: str* *= '/Users/paul.bridi/Projects/MLServer/docs-gb/.metrics'* {#mlserver.settings.Settings.metrics_dir}
Directory used to share metrics across parallel workers.
Equivalent to the PROMETHEUS_MULTIPROC_DIR env var in
prometheus-client.
Note that this won’t be used if the parallel_workers flag is disabled.
By default, the .metrics folder of the current working directory will be
used.
#### *field* metrics_endpoint *: str | None* *= '/metrics'* {#mlserver.settings.Settings.metrics_endpoint}
Endpoint used to expose Prometheus metrics. Alternatively, can be set to
None to disable it.
#### *field* metrics_port *: int* *= 8082* {#mlserver.settings.Settings.metrics_port}
Port used to expose metrics endpoint.
#### *field* metrics_rest_server_prefix *: str* *= 'rest_server'* {#mlserver.settings.Settings.metrics_rest_server_prefix}
Metrics rest server string prefix to be exported.
#### *field* model_repository_implementation *: ImportString | None* *= None* {#mlserver.settings.Settings.model_repository_implementation}
*Python path* to the inference runtime to model repository (e.g.
`mlserver.repository.repository.SchemalessModelRepository`).
#### *field* model_repository_implementation_args *: dict* *= {}* {#mlserver.settings.Settings.model_repository_implementation_args}
Extra parameters for model repository.
#### *field* model_repository_root *: str* *= '.'* {#mlserver.settings.Settings.model_repository_root}
Root of the model repository, where we will search for models.
#### *field* parallel_workers *: int* *= 1* {#mlserver.settings.Settings.parallel_workers}
When parallel inference is enabled, number of workers to run inference
across.
#### *field* parallel_workers_timeout *: int* *= 5* {#mlserver.settings.Settings.parallel_workers_timeout}
Grace timeout to wait until the workers shut down when stopping MLServer.
#### *field* root_path *: str* *= ''* {#mlserver.settings.Settings.root_path}
Set the ASGI root_path for applications submounted below a given URL path.
#### *field* server_name *: str* *= 'mlserver'* {#mlserver.settings.Settings.server_name}
Name of the server.
#### *field* server_version *: str* *= '1.7.0.dev0'* {#mlserver.settings.Settings.server_version}
Version of the server.
#### *field* tracing_server *: str | None* *= None* {#mlserver.settings.Settings.tracing_server}
Server name used to export OpenTelemetry tracing to collector service.
#### *field* use_structured_logging *: bool* *= False* {#mlserver.settings.Settings.use_structured_logging}
Use JSON-formatted structured logging instead of default format.
#### model_post_init(context,) {#mlserver.settings.Settings.model_post_init}
This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that’s what pydantic-core passes when calling it.

* **Parameters:**
  * **self** (*BaseModel*) – The BaseModel instance.
  * **context** (*Any*) – The context.
* **Return type:**
  None
