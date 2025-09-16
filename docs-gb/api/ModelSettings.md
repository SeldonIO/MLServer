# ModelSettings

### Config

| Attribute | Type | Default |
|-----------|------|---------|
| `extra` | `str` | `"ignore"` |
| `env_prefix` | `str` | `"MLSERVER_MODEL_"` |
| `env_file` | `str` | `".env"` |
| `protected_namespaces` | `tuple` | `('model_', 'settings_')` |

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `cache_enabled` | `bool` | `False` | Enable caching for a specific model. This parameter can be used to disable cache for a specific model, if the server-level caching is enabled. If the server-level caching is disabled, this parameter value will have no effect. |
| `implementation_` | `str` | `-` | *Python path* to the inference runtime to use to serve this model (e.g. `mlserver_sklearn.SKLearnModel`). |
| `inputs` | `List[MetadataTensor]` | `<factory>` | Metadata about the inputs accepted by the model. |
| `max_batch_size` | `int` | `0` | When adaptive batching is enabled, maximum number of requests to group together in a single batch. |
| `max_batch_time` | `float` | `0.0` | When adaptive batching is enabled, maximum amount of time (in seconds) to wait for enough requests to build a full batch. |
| `name` | `str` | `''` | Name of the model. |
| `outputs` | `List[MetadataTensor]` | `<factory>` | Metadata about the outputs returned by the model. |
| `parallel_workers` | `Optional[int]` | `None` | Use the `parallel_workers` field in the server-wide settings instead. |
| `parameters` | `Optional[ModelParameters]` | `None` | Extra parameters for each instance of this model. |
| `platform` | `str` | `''` | Framework used to train and serialise the model (e.g. sklearn). |
| `versions` | `List[str]` | `<factory>` | Versions of dependencies used to train the model (e.g. sklearn/0.20.1). |
| `warm_workers` | `bool` | `False` | Inference workers will now always be `warmed up` at start time. |
