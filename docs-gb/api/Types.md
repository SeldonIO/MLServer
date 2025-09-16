# Types

## Methods

# Module `mlserver.types`

## Class `Datatype`

### Methods

## Class `InferenceErrorResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `InferenceRequest`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `InferenceResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `MetadataModelErrorResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `MetadataModelResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `MetadataServerErrorResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `MetadataServerResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `MetadataTensor`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `Parameters`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RepositoryIndexRequest`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RepositoryIndexResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(root: 'RootModelRootType', _fields_set: 'set[str] | None' = None) -> 'Self'
```
Create a new model using the provided root object and update fields set.

Args:
    root: The root object of the model.
    _fields_set: The set of fields to be updated.

Returns:
    The new model.

Raises:
    NotImplemented: If the model is not a subclass of `RootModel`.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False) -> 'str'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RepositoryIndexResponseItem`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RepositoryLoadErrorResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RepositoryUnloadErrorResponse`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RequestInput`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `RequestOutput`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `ResponseOutput`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.

Returns:
    A new instance of the `Model` class with validated data.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-

## Class `State`

### Methods

## Class `TensorData`

### Methods

### `construct`
```python
construct(_fields_set: 'set[str] | None' = None, **values: 'Any') -> 'Self'
```
-

### `copy`
```python
copy(self, *, include: 'AbstractSetIntStr | MappingIntStrAny | None' = None, exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None, update: 'Dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns:
    A copy of the model with included, excluded and updated fields as specified.

### `dict`
```python
dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'
```
-

### `from_orm`
```python
from_orm(obj: 'Any') -> 'Self'
```
-

### `json`
```python
json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'
```
-

### `model_construct`
```python
model_construct(root: 'RootModelRootType', _fields_set: 'set[str] | None' = None) -> 'Self'
```
Create a new model using the provided root object and update fields set.

Args:
    root: The root object of the model.
    _fields_set: The set of fields to be updated.

Returns:
    The new model.

Raises:
    NotImplemented: If the model is not a subclass of `RootModel`.

### `model_copy`
```python
model_copy(self, *, update: 'dict[str, Any] | None' = None, deep: 'bool' = False) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

Args:
    update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.

Returns:
    New model instance.

### `model_dump`
```python
model_dump(self, *, mode: "Literal['json', 'python'] | str" = 'python', include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False) -> 'dict[str, Any]'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args:
    mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A dictionary representation of the model.

### `model_dump_json`
```python
model_dump_json(self, *, indent: 'int | None' = None, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, context: 'Any | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, round_trip: 'bool' = False, warnings: "bool | Literal['none', 'warn', 'error']" = True, serialize_as_any: 'bool' = False) -> 'str'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

Returns:
    A JSON string representation of the model.

### `model_json_schema`
```python
model_json_schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: 'JsonSchemaMode' = 'validation') -> 'dict[str, Any]'
```
Generates a JSON schema for a model class.

Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.

Returns:
    The JSON schema for the given model class.

### `model_parametrized_name`
```python
model_parametrized_name(params: 'tuple[type[Any], ...]') -> 'str'
```
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args:
    params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.

Returns:
    String representing the new class where `params` are passed to `cls` as type variables.

Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.

### `model_post_init`
```python
model_post_init(self, _BaseModel__context: 'Any') -> 'None'
```
Override this method to perform additional initialization after `__init__` and `model_construct`.
This is useful if you want to do some validation that requires the entire model to be initialized.

### `model_rebuild`
```python
model_rebuild(*, force: 'bool' = False, raise_errors: 'bool' = True, _parent_namespace_depth: 'int' = 2, _types_namespace: 'dict[str, Any] | None' = None) -> 'bool | None'
```
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.

Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### `model_validate`
```python
model_validate(obj: 'Any', *, strict: 'bool | None' = None, from_attributes: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate a pydantic model instance.

Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.

Raises:
    ValidationError: If the object could not be validated.

Returns:
    The validated model instance.

### `model_validate_json`
```python
model_validate_json(json_data: 'str | bytes | bytearray', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

### `model_validate_strings`
```python
model_validate_strings(obj: 'Any', *, strict: 'bool | None' = None, context: 'Any | None' = None) -> 'Self'
```
Validate the given object with string data against the Pydantic model.

Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.

Returns:
    The validated Pydantic model.

### `parse_file`
```python
parse_file(path: 'str | Path', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `parse_obj`
```python
parse_obj(obj: 'Any') -> 'Self'
```
-

### `parse_raw`
```python
parse_raw(b: 'str | bytes', *, content_type: 'str | None' = None, encoding: 'str' = 'utf8', proto: 'DeprecatedParseProtocol | None' = None, allow_pickle: 'bool' = False) -> 'Self'
```
-

### `schema`
```python
schema(by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}') -> 'Dict[str, Any]'
```
-

### `schema_json`
```python
schema_json(*, by_alias: 'bool' = True, ref_template: 'str' = '#/$defs/{model}', **dumps_kwargs: 'Any') -> 'str'
```
-

### `update_forward_refs`
```python
update_forward_refs(**localns: 'Any') -> 'None'
```
-

### `validate`
```python
validate(value: 'Any') -> 'Self'
```
-


