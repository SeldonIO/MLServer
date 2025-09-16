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


### Class `InferenceResponse`

```python
class InferenceResponse
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


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


### Class `MetadataTensor`

```python
class MetadataTensor
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


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


### Class `Parameters`

```python
class Parameters
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RequestInput`

```python
class RequestInput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `RequestOutput`

```python
class RequestOutput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


### Class `ResponseOutput`

```python
class ResponseOutput
```

Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525


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



