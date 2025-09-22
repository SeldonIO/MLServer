# Module `mlserver.settings`


## Class `BaseSettings`


**Description:**
Base class for settings, allowing values to be overridden by environment variables.
This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

**Parameters:**
- `_case_sensitive` (unknown): Whether environment and CLI variable names should be read with case-sensitivity.
Defaults to `None`.
- `_nested_model_default_partial_update` (unknown): Whether to allow partial updates on nested model default object fields.
Defaults to `False`.
- `_env_prefix` (unknown): Prefix for all environment variables. Defaults to `None`.
- `_env_file` (unknown): The env file(s) to load settings values from. Defaults to `Path('')`, which
means that the value from `model_config['env_file']` should be used. You can also pass
`None` to indicate that environment variables should not be loaded from an env file.
- `_env_file_encoding` (unknown): The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
- `_env_ignore_empty` (unknown): Ignore environment variables where the value is an empty string. Default to `False`.
- `_env_nested_delimiter` (unknown): The nested env values delimiter. Defaults to `None`.
- `_env_nested_max_split` (unknown): The nested env values maximum nesting. Defaults to `None`, which means no limit.
- `_env_parse_none_str` (unknown): The env string value that should be parsed (e.g. "null", "void", "None", etc.)
into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
- `_env_parse_enums` (unknown): Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
- `_cli_prog_name` (unknown): The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
Otherwise, defaults to sys.argv[0].
- `_cli_parse_args` (unknown): The list of CLI arguments to parse. Defaults to None.
If set to `True`, defaults to sys.argv[1:].
- `_cli_settings_source` (unknown): Override the default CLI settings source with a user defined instance. Defaults to None.
- `_cli_parse_none_str` (unknown): The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
`None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
_cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
- `_cli_hide_none_type` (unknown): Hide `None` values in CLI help text. Defaults to `False`.
- `_cli_avoid_json` (unknown): Avoid complex JSON objects in CLI help text. Defaults to `False`.
- `_cli_enforce_required` (unknown): Enforce required fields at the CLI. Defaults to `False`.
- `_cli_use_class_docs_for_groups` (unknown): Use class docstrings in CLI group help text instead of field descriptions.
Defaults to `False`.
- `_cli_exit_on_error` (unknown): Determines whether or not the internal parser exits with error info when an error occurs.
Defaults to `True`.
- `_cli_prefix` (unknown): The root parser command line arguments prefix. Defaults to "".
- `_cli_flag_prefix_char` (unknown): The flag prefix character to use for CLI optional arguments. Defaults to '-'.
- `_cli_implicit_flags` (unknown): Whether `bool` fields should be implicitly converted into CLI boolean flags.
(e.g. --flag, --no-flag). Defaults to `False`.
- `_cli_ignore_unknown_args` (unknown): Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
- `_cli_kebab_case` (unknown): CLI args use kebab case. Defaults to `False`.
- `_cli_shortcuts` (unknown): Mapping of target field name to alias names. Defaults to `None`.
- `_secrets_dir` (unknown): The secret files directory or a sequence of directories. Defaults to `None`.

### Method `copy`


**Signature:** `copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
Returns a copy of the model.
!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**
- `include` (unknown): Optional set or mapping specifying which fields to include in the copied model.
- `exclude` (unknown): Optional set or mapping specifying which fields to exclude in the copied model.
- `update` (unknown): Optional dictionary of field-value pairs to override field values in the copied model.
- `deep` (unknown): If True, the values of fields that are Pydantic models will be deep-copied.

**Returns:**
- (unknown): A copy of the model with included, excluded and updated fields as specified.

### Method `dict`


**Signature:** `dict(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `json`


**Signature:** `json(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `model_copy`


**Signature:** `model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
!!! abstract "Usage Documentation"
[`model_copy`](../concepts/serialization.md#model_copy)

Returns a copy of the model.

!!! note
    The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
    might have unexpected side effects if you store anything in it, on top of the model
    fields (e.g. the value of [cached properties][functools.cached_property]).

**Parameters:**
- `update` (unknown): Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
- `deep` (unknown): Set to `True` to make a deep copy of the model.

**Returns:**
- (unknown): New model instance.

### Method `model_dump`


**Signature:** `model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**
- `mode` (unknown): The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
- `include` (unknown): A set of fields to include in the output.
- `exclude` (unknown): A set of fields to exclude from the output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to use the field's alias in the dictionary key if defined.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A dictionary representation of the model.

### Method `model_dump_json`


**Signature:** `model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'str'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**
- `indent` (unknown): Indentation to use in the JSON output. If None is passed, the output will be compact.
- `include` (unknown): Field(s) to include in the JSON output.
- `exclude` (unknown): Field(s) to exclude from the JSON output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to serialize using field aliases.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A JSON string representation of the model.

### Method `model_post_init`


**Signature:** `model_post_init(self, context: 'Any', /) -> 'None'`


**Description:**
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

## Class `CORSSettings`


**Description:**
Base class for settings, allowing values to be overridden by environment variables.
This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

**Parameters:**
- `_case_sensitive` (unknown): Whether environment and CLI variable names should be read with case-sensitivity.
Defaults to `None`.
- `_nested_model_default_partial_update` (unknown): Whether to allow partial updates on nested model default object fields.
Defaults to `False`.
- `_env_prefix` (unknown): Prefix for all environment variables. Defaults to `None`.
- `_env_file` (unknown): The env file(s) to load settings values from. Defaults to `Path('')`, which
means that the value from `model_config['env_file']` should be used. You can also pass
`None` to indicate that environment variables should not be loaded from an env file.
- `_env_file_encoding` (unknown): The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
- `_env_ignore_empty` (unknown): Ignore environment variables where the value is an empty string. Default to `False`.
- `_env_nested_delimiter` (unknown): The nested env values delimiter. Defaults to `None`.
- `_env_nested_max_split` (unknown): The nested env values maximum nesting. Defaults to `None`, which means no limit.
- `_env_parse_none_str` (unknown): The env string value that should be parsed (e.g. "null", "void", "None", etc.)
into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
- `_env_parse_enums` (unknown): Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
- `_cli_prog_name` (unknown): The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
Otherwise, defaults to sys.argv[0].
- `_cli_parse_args` (unknown): The list of CLI arguments to parse. Defaults to None.
If set to `True`, defaults to sys.argv[1:].
- `_cli_settings_source` (unknown): Override the default CLI settings source with a user defined instance. Defaults to None.
- `_cli_parse_none_str` (unknown): The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
`None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
_cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
- `_cli_hide_none_type` (unknown): Hide `None` values in CLI help text. Defaults to `False`.
- `_cli_avoid_json` (unknown): Avoid complex JSON objects in CLI help text. Defaults to `False`.
- `_cli_enforce_required` (unknown): Enforce required fields at the CLI. Defaults to `False`.
- `_cli_use_class_docs_for_groups` (unknown): Use class docstrings in CLI group help text instead of field descriptions.
Defaults to `False`.
- `_cli_exit_on_error` (unknown): Determines whether or not the internal parser exits with error info when an error occurs.
Defaults to `True`.
- `_cli_prefix` (unknown): The root parser command line arguments prefix. Defaults to "".
- `_cli_flag_prefix_char` (unknown): The flag prefix character to use for CLI optional arguments. Defaults to '-'.
- `_cli_implicit_flags` (unknown): Whether `bool` fields should be implicitly converted into CLI boolean flags.
(e.g. --flag, --no-flag). Defaults to `False`.
- `_cli_ignore_unknown_args` (unknown): Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
- `_cli_kebab_case` (unknown): CLI args use kebab case. Defaults to `False`.
- `_cli_shortcuts` (unknown): Mapping of target field name to alias names. Defaults to `None`.
- `_secrets_dir` (unknown): The secret files directory or a sequence of directories. Defaults to `None`.

### Method `copy`


**Signature:** `copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
Returns a copy of the model.
!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**
- `include` (unknown): Optional set or mapping specifying which fields to include in the copied model.
- `exclude` (unknown): Optional set or mapping specifying which fields to exclude in the copied model.
- `update` (unknown): Optional dictionary of field-value pairs to override field values in the copied model.
- `deep` (unknown): If True, the values of fields that are Pydantic models will be deep-copied.

**Returns:**
- (unknown): A copy of the model with included, excluded and updated fields as specified.

### Method `dict`


**Signature:** `dict(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `json`


**Signature:** `json(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `model_copy`


**Signature:** `model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
!!! abstract "Usage Documentation"
[`model_copy`](../concepts/serialization.md#model_copy)

Returns a copy of the model.

!!! note
    The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
    might have unexpected side effects if you store anything in it, on top of the model
    fields (e.g. the value of [cached properties][functools.cached_property]).

**Parameters:**
- `update` (unknown): Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
- `deep` (unknown): Set to `True` to make a deep copy of the model.

**Returns:**
- (unknown): New model instance.

### Method `model_dump`


**Signature:** `model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**
- `mode` (unknown): The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
- `include` (unknown): A set of fields to include in the output.
- `exclude` (unknown): A set of fields to exclude from the output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to use the field's alias in the dictionary key if defined.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A dictionary representation of the model.

### Method `model_dump_json`


**Signature:** `model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'str'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**
- `indent` (unknown): Indentation to use in the JSON output. If None is passed, the output will be compact.
- `include` (unknown): Field(s) to include in the JSON output.
- `exclude` (unknown): Field(s) to exclude from the JSON output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to serialize using field aliases.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A JSON string representation of the model.

### Method `model_post_init`


**Signature:** `model_post_init(self, context: 'Any', /) -> 'None'`


**Description:**
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

## Class `ModelParameters`


**Description:**
Parameters that apply only to a particular instance of a model.
This can include things like model weights, or arbitrary ``extra``
parameters particular to the underlying inference runtime.
The main difference with respect to ``ModelSettings`` is that parameters
can change on each instance (e.g. each version) of the model.

### Method `copy`


**Signature:** `copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
Returns a copy of the model.
!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**
- `include` (unknown): Optional set or mapping specifying which fields to include in the copied model.
- `exclude` (unknown): Optional set or mapping specifying which fields to exclude in the copied model.
- `update` (unknown): Optional dictionary of field-value pairs to override field values in the copied model.
- `deep` (unknown): If True, the values of fields that are Pydantic models will be deep-copied.

**Returns:**
- (unknown): A copy of the model with included, excluded and updated fields as specified.

### Method `dict`


**Signature:** `dict(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `json`


**Signature:** `json(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `model_copy`


**Signature:** `model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
!!! abstract "Usage Documentation"
[`model_copy`](../concepts/serialization.md#model_copy)

Returns a copy of the model.

!!! note
    The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
    might have unexpected side effects if you store anything in it, on top of the model
    fields (e.g. the value of [cached properties][functools.cached_property]).

**Parameters:**
- `update` (unknown): Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
- `deep` (unknown): Set to `True` to make a deep copy of the model.

**Returns:**
- (unknown): New model instance.

### Method `model_dump`


**Signature:** `model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**
- `mode` (unknown): The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
- `include` (unknown): A set of fields to include in the output.
- `exclude` (unknown): A set of fields to exclude from the output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to use the field's alias in the dictionary key if defined.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A dictionary representation of the model.

### Method `model_dump_json`


**Signature:** `model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'str'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**
- `indent` (unknown): Indentation to use in the JSON output. If None is passed, the output will be compact.
- `include` (unknown): Field(s) to include in the JSON output.
- `exclude` (unknown): Field(s) to exclude from the JSON output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to serialize using field aliases.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A JSON string representation of the model.

### Method `model_post_init`


**Signature:** `model_post_init(self, context: 'Any', /) -> 'None'`


**Description:**
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### Method `set_inference_pool_gid`


**Signature:** `set_inference_pool_gid(self) -> Self`


**Description:**
*No docstring available.*

## Class `ModelSettings`


**Description:**
Base class for settings, allowing values to be overridden by environment variables.
This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

**Parameters:**
- `_case_sensitive` (unknown): Whether environment and CLI variable names should be read with case-sensitivity.
Defaults to `None`.
- `_nested_model_default_partial_update` (unknown): Whether to allow partial updates on nested model default object fields.
Defaults to `False`.
- `_env_prefix` (unknown): Prefix for all environment variables. Defaults to `None`.
- `_env_file` (unknown): The env file(s) to load settings values from. Defaults to `Path('')`, which
means that the value from `model_config['env_file']` should be used. You can also pass
`None` to indicate that environment variables should not be loaded from an env file.
- `_env_file_encoding` (unknown): The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
- `_env_ignore_empty` (unknown): Ignore environment variables where the value is an empty string. Default to `False`.
- `_env_nested_delimiter` (unknown): The nested env values delimiter. Defaults to `None`.
- `_env_nested_max_split` (unknown): The nested env values maximum nesting. Defaults to `None`, which means no limit.
- `_env_parse_none_str` (unknown): The env string value that should be parsed (e.g. "null", "void", "None", etc.)
into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
- `_env_parse_enums` (unknown): Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
- `_cli_prog_name` (unknown): The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
Otherwise, defaults to sys.argv[0].
- `_cli_parse_args` (unknown): The list of CLI arguments to parse. Defaults to None.
If set to `True`, defaults to sys.argv[1:].
- `_cli_settings_source` (unknown): Override the default CLI settings source with a user defined instance. Defaults to None.
- `_cli_parse_none_str` (unknown): The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
`None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
_cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
- `_cli_hide_none_type` (unknown): Hide `None` values in CLI help text. Defaults to `False`.
- `_cli_avoid_json` (unknown): Avoid complex JSON objects in CLI help text. Defaults to `False`.
- `_cli_enforce_required` (unknown): Enforce required fields at the CLI. Defaults to `False`.
- `_cli_use_class_docs_for_groups` (unknown): Use class docstrings in CLI group help text instead of field descriptions.
Defaults to `False`.
- `_cli_exit_on_error` (unknown): Determines whether or not the internal parser exits with error info when an error occurs.
Defaults to `True`.
- `_cli_prefix` (unknown): The root parser command line arguments prefix. Defaults to "".
- `_cli_flag_prefix_char` (unknown): The flag prefix character to use for CLI optional arguments. Defaults to '-'.
- `_cli_implicit_flags` (unknown): Whether `bool` fields should be implicitly converted into CLI boolean flags.
(e.g. --flag, --no-flag). Defaults to `False`.
- `_cli_ignore_unknown_args` (unknown): Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
- `_cli_kebab_case` (unknown): CLI args use kebab case. Defaults to `False`.
- `_cli_shortcuts` (unknown): Mapping of target field name to alias names. Defaults to `None`.
- `_secrets_dir` (unknown): The secret files directory or a sequence of directories. Defaults to `None`.

### Method `copy`


**Signature:** `copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
Returns a copy of the model.
!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**
- `include` (unknown): Optional set or mapping specifying which fields to include in the copied model.
- `exclude` (unknown): Optional set or mapping specifying which fields to exclude in the copied model.
- `update` (unknown): Optional dictionary of field-value pairs to override field values in the copied model.
- `deep` (unknown): If True, the values of fields that are Pydantic models will be deep-copied.

**Returns:**
- (unknown): A copy of the model with included, excluded and updated fields as specified.

### Method `dict`


**Signature:** `dict(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `json`


**Signature:** `json(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `model_copy`


**Signature:** `model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
!!! abstract "Usage Documentation"
[`model_copy`](../concepts/serialization.md#model_copy)

Returns a copy of the model.

!!! note
    The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
    might have unexpected side effects if you store anything in it, on top of the model
    fields (e.g. the value of [cached properties][functools.cached_property]).

**Parameters:**
- `update` (unknown): Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
- `deep` (unknown): Set to `True` to make a deep copy of the model.

**Returns:**
- (unknown): New model instance.

### Method `model_dump`


**Signature:** `model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**
- `mode` (unknown): The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
- `include` (unknown): A set of fields to include in the output.
- `exclude` (unknown): A set of fields to exclude from the output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to use the field's alias in the dictionary key if defined.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A dictionary representation of the model.

### Method `model_dump_json`


**Signature:** `model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'str'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**
- `indent` (unknown): Indentation to use in the JSON output. If None is passed, the output will be compact.
- `include` (unknown): Field(s) to include in the JSON output.
- `exclude` (unknown): Field(s) to exclude from the JSON output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to serialize using field aliases.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A JSON string representation of the model.

### Method `model_post_init`


**Signature:** `model_post_init(self: 'BaseModel', context: 'Any', /) -> 'None'`


**Description:**
This function is meant to behave like a BaseModel method to initialise private attributes.
It takes context as an argument since that's what pydantic-core passes when calling it.

**Parameters:**
- `self` (unknown): The BaseModel instance.
- `context` (unknown): The context.

## Class `Settings`


**Description:**
Base class for settings, allowing values to be overridden by environment variables.
This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

**Parameters:**
- `_case_sensitive` (unknown): Whether environment and CLI variable names should be read with case-sensitivity.
Defaults to `None`.
- `_nested_model_default_partial_update` (unknown): Whether to allow partial updates on nested model default object fields.
Defaults to `False`.
- `_env_prefix` (unknown): Prefix for all environment variables. Defaults to `None`.
- `_env_file` (unknown): The env file(s) to load settings values from. Defaults to `Path('')`, which
means that the value from `model_config['env_file']` should be used. You can also pass
`None` to indicate that environment variables should not be loaded from an env file.
- `_env_file_encoding` (unknown): The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
- `_env_ignore_empty` (unknown): Ignore environment variables where the value is an empty string. Default to `False`.
- `_env_nested_delimiter` (unknown): The nested env values delimiter. Defaults to `None`.
- `_env_nested_max_split` (unknown): The nested env values maximum nesting. Defaults to `None`, which means no limit.
- `_env_parse_none_str` (unknown): The env string value that should be parsed (e.g. "null", "void", "None", etc.)
into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
- `_env_parse_enums` (unknown): Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
- `_cli_prog_name` (unknown): The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
Otherwise, defaults to sys.argv[0].
- `_cli_parse_args` (unknown): The list of CLI arguments to parse. Defaults to None.
If set to `True`, defaults to sys.argv[1:].
- `_cli_settings_source` (unknown): Override the default CLI settings source with a user defined instance. Defaults to None.
- `_cli_parse_none_str` (unknown): The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
`None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
_cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
- `_cli_hide_none_type` (unknown): Hide `None` values in CLI help text. Defaults to `False`.
- `_cli_avoid_json` (unknown): Avoid complex JSON objects in CLI help text. Defaults to `False`.
- `_cli_enforce_required` (unknown): Enforce required fields at the CLI. Defaults to `False`.
- `_cli_use_class_docs_for_groups` (unknown): Use class docstrings in CLI group help text instead of field descriptions.
Defaults to `False`.
- `_cli_exit_on_error` (unknown): Determines whether or not the internal parser exits with error info when an error occurs.
Defaults to `True`.
- `_cli_prefix` (unknown): The root parser command line arguments prefix. Defaults to "".
- `_cli_flag_prefix_char` (unknown): The flag prefix character to use for CLI optional arguments. Defaults to '-'.
- `_cli_implicit_flags` (unknown): Whether `bool` fields should be implicitly converted into CLI boolean flags.
(e.g. --flag, --no-flag). Defaults to `False`.
- `_cli_ignore_unknown_args` (unknown): Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
- `_cli_kebab_case` (unknown): CLI args use kebab case. Defaults to `False`.
- `_cli_shortcuts` (unknown): Mapping of target field name to alias names. Defaults to `None`.
- `_secrets_dir` (unknown): The secret files directory or a sequence of directories. Defaults to `None`.

### Method `copy`


**Signature:** `copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
Returns a copy of the model.
!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```python {test="skip" lint="skip"}
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**
- `include` (unknown): Optional set or mapping specifying which fields to include in the copied model.
- `exclude` (unknown): Optional set or mapping specifying which fields to exclude in the copied model.
- `update` (unknown): Optional dictionary of field-value pairs to override field values in the copied model.
- `deep` (unknown): If True, the values of fields that are Pydantic models will be deep-copied.

**Returns:**
- (unknown): A copy of the model with included, excluded and updated fields as specified.

### Method `dict`


**Signature:** `dict(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `json`


**Signature:** `json(self, by_alias=True, exclude_unset=True, exclude_none=True, **kwargs)`


**Description:**
Ensure that aliases are used, and that unset / none fields are ignored.

### Method `model_copy`


**Signature:** `model_copy(self, *, update: 'Mapping[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'`


**Description:**
!!! abstract "Usage Documentation"
[`model_copy`](../concepts/serialization.md#model_copy)

Returns a copy of the model.

!!! note
    The underlying instance's [`__dict__`][object.__dict__] attribute is copied. This
    might have unexpected side effects if you store anything in it, on top of the model
    fields (e.g. the value of [cached properties][functools.cached_property]).

**Parameters:**
- `update` (unknown): Values to change/add in the new model. Note: the data is not validated
before creating the new model. You should trust this data.
- `deep` (unknown): Set to `True` to make a deep copy of the model.

**Returns:**
- (unknown): New model instance.

### Method `model_dump`


**Signature:** `model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump`](../concepts/serialization.md#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**
- `mode` (unknown): The mode in which `to_python` should run.
If mode is 'json', the output will only contain JSON serializable types.
If mode is 'python', the output may contain non-JSON-serializable Python objects.
- `include` (unknown): A set of fields to include in the output.
- `exclude` (unknown): A set of fields to exclude from the output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to use the field's alias in the dictionary key if defined.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A dictionary representation of the model.

### Method `model_dump_json`


**Signature:** `model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool | None' = None, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, fallback: 'Callable[[Any], Any] | None' = None, serialize_as_any: 'bool' = False) -> 'str'`


**Description:**
!!! abstract "Usage Documentation"
[`model_dump_json`](../concepts/serialization.md#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**
- `indent` (unknown): Indentation to use in the JSON output. If None is passed, the output will be compact.
- `include` (unknown): Field(s) to include in the JSON output.
- `exclude` (unknown): Field(s) to exclude from the JSON output.
- `context` (unknown): Additional context to pass to the serializer.
- `by_alias` (unknown): Whether to serialize using field aliases.
- `exclude_unset` (unknown): Whether to exclude fields that have not been explicitly set.
- `exclude_defaults` (unknown): Whether to exclude fields that are set to their default value.
- `exclude_none` (unknown): Whether to exclude fields that have a value of `None`.
- `round_trip` (unknown): If True, dumped values should be valid as input for non-idempotent types such as Json[T].
- `warnings` (unknown): How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
- `fallback` (unknown): A function to call when an unknown value is encountered. If not provided,
a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
- `serialize_as_any` (unknown): Whether to serialize fields with duck-typing serialization behavior.

**Returns:**
- (unknown): A JSON string representation of the model.

### Method `model_post_init`


**Signature:** `model_post_init(self: 'BaseModel', context: 'Any', /) -> 'None'`


**Description:**
This function is meant to behave like a BaseModel method to initialise private attributes.
It takes context as an argument since that's what pydantic-core passes when calling it.

**Parameters:**
- `self` (unknown): The BaseModel instance.
- `context` (unknown): The context.
