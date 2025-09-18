# ModelParameters

### Config

| Attribute | Type | Default |
|-----------|------|---------|
| `extra` | `str` | `"allow"` |
| `env_prefix` | `str` | `"MLSERVER_MODEL_"` |
| `env_file` | `str` | `".env"` |
| `protected_namespaces` | `tuple` | `('model_', 'settings_')` |

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `autogenerate_inference_pool_gid` | `bool` | `False` | Flag to autogenerate the inference pool group id for this model. |
| `content_type` | `Optional[str]` | `None` | Default content type to use for requests and responses. |
| `environment_path` | `Optional[str]` | `None` | Path to a directory that contains the python environment to be used to load this model. |
| `environment_tarball` | `Optional[str]` | `None` | Path to the environment tarball which should be used to load this model. |
| `extra` | `Optional[dict]` | `<factory>` | Arbitrary settings, dependent on the inference runtime implementation. |
| `format` | `Optional[str]` | `None` | Format of the model (only available on certain runtimes). |
| `inference_pool_gid` | `Optional[str]` | `None` | Inference pool group id to be used to serve this model. |
| `uri` | `Optional[str]` | `None` | URI where the model artifacts can be found. This path must be either absolute or relative to where MLServer is running. |
| `version` | `Optional[str]` | `None` | Version of the model. |
