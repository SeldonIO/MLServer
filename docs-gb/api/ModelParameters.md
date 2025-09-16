# ModelParameters

## Fields

### Config

| Attribute | Type | Default |
|-----------|------|---------|
| `extra` | `str` | `"ignore"` |
| `env_prefix` | `str` | `"MLSERVER_"` |
| `env_file` | `str` | `".env"` |
| `protected_namespaces` | `tuple` | `"()"` |

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `autogenerate_inference_pool_gid` | `bool` | `False` | Flag to autogenerate the inference pool group id for this model. |
| `content_type` | `Optional` | `-` | Default content type to use for requests and responses. |
| `environment_path` | `Optional` | `-` | Path to a directory that contains the python environment to be used to load this model. |
| `environment_tarball` | `Optional` | `-` | Path to the environment tarball which should be used to load this model. |
| `extra` | `Optional` | `PydanticUndefined` | Arbitrary settings, dependent on the inference runtime implementation. |
| `format` | `Optional` | `-` | Format of the model (only available on certain runtimes). |
| `inference_pool_gid` | `Optional` | `-` | Inference pool group id to be used to serve this model. |
| `uri` | `Optional` | `-` | URI where the model artifacts can be found. This path must be either absolute or relative to where MLServer is running. |
| `version` | `Optional` | `-` | Version of the model. |

