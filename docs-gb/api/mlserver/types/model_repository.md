# Module `mlserver.types.model_repository`


## Class `RepositoryIndexRequest`


**Description:**
Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

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


**Signature:** `dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'`


**Description:**
*No docstring available.*

### Method `json`


**Signature:** `json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'`


**Description:**
*No docstring available.*

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


**Signature:** `model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)`


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


**Signature:** `model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)`


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

## Class `RepositoryIndexResponse`


**Description:**
!!! abstract "Usage Documentation"
[`RootModel` and Custom Root Types](../concepts/models.md#rootmodel-and-custom-root-types)

A Pydantic `BaseModel` for the root object of the model.

**Parameters:**
- `root` (unknown): The root object of the model.
- `__pydantic_root_model__` (unknown): Whether the model is a RootModel.
- `__pydantic_private__` (unknown): Private fields in the model.
- `__pydantic_extra__` (unknown): Extra fields in the model.

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


**Signature:** `dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'`


**Description:**
*No docstring available.*

### Method `json`


**Signature:** `json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'`


**Description:**
*No docstring available.*

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

## Class `RepositoryIndexResponseItem`


**Description:**
Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

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


**Signature:** `dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'`


**Description:**
*No docstring available.*

### Method `json`


**Signature:** `json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'`


**Description:**
*No docstring available.*

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


**Signature:** `model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)`


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


**Signature:** `model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)`


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

## Class `RepositoryLoadErrorResponse`


**Description:**
Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

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


**Signature:** `dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'`


**Description:**
*No docstring available.*

### Method `json`


**Signature:** `json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'`


**Description:**
*No docstring available.*

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


**Signature:** `model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)`


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


**Signature:** `model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)`


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

## Class `RepositoryUnloadErrorResponse`


**Description:**
Override Pydantic's BaseModel class to ensure all payloads exclude unset
fields by default.

From:
    https://github.com/pydantic/pydantic/issues/1387#issuecomment-612901525

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


**Signature:** `dict(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False) -> 'Dict[str, Any]'`


**Description:**
*No docstring available.*

### Method `json`


**Signature:** `json(self, *, include: 'IncEx | None' = None, exclude: 'IncEx | None' = None, by_alias: 'bool' = False, exclude_unset: 'bool' = False, exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, encoder: 'Callable[[Any], Any] | None' = PydanticUndefined, models_as_dict: 'bool' = PydanticUndefined, **dumps_kwargs: 'Any') -> 'str'`


**Description:**
*No docstring available.*

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


**Signature:** `model_dump(self, exclude_unset=True, exclude_none=True, **kwargs)`


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


**Signature:** `model_dump_json(self, exclude_unset=True, exclude_none=True, **kwargs)`


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

## Class `State`


**Description:**
Create a collection of name/value pairs.
Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)
[<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]

Methods can be added to enumerations, and members can have their own
attributes -- see the documentation for details.
