# Module `mlserver.parallel.messages`


## Class `Message`


**Description:**
!!! abstract "Usage Documentation"
[Models](../concepts/models.md)

A base class for creating Pydantic models.

**Parameters:**
- `__class_vars__` (unknown): The names of the class variables defined on the model.
- `__private_attributes__` (unknown): Metadata about the private attributes of the model.
- `__signature__` (unknown): The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
- `__pydantic_complete__` (unknown): Whether model building is completed, or if there are still undefined fields.
- `__pydantic_core_schema__` (unknown): The core schema of the model.
- `__pydantic_custom_init__` (unknown): Whether the model has a custom `__init__` function.
- `__pydantic_decorators__` (unknown): Metadata containing the decorators defined on the model.
This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
- `__pydantic_generic_metadata__` (unknown): Metadata for generic models; contains data used for a similar purpose to
__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
- `__pydantic_parent_namespace__` (unknown): Parent namespace of the model, used for automatic rebuilding of models.
- `__pydantic_post_init__` (unknown): The name of the post-init method for the model, if defined.
- `__pydantic_root_model__` (unknown): Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
- `__pydantic_serializer__` (unknown): The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
- `__pydantic_validator__` (unknown): The `pydantic-core` `SchemaValidator` used to validate instances of the model.
- `__pydantic_fields__` (unknown): A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
- `__pydantic_computed_fields__` (unknown): A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
- `__pydantic_extra__` (unknown): A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
is set to `'allow'`.
- `__pydantic_fields_set__` (unknown): The names of fields explicitly set during instantiation.
- `__pydantic_private__` (unknown): Values of private attributes set on the model instance.

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

## Class `ModelRequestMessage`


**Description:**
!!! abstract "Usage Documentation"
[Models](../concepts/models.md)

A base class for creating Pydantic models.

**Parameters:**
- `__class_vars__` (unknown): The names of the class variables defined on the model.
- `__private_attributes__` (unknown): Metadata about the private attributes of the model.
- `__signature__` (unknown): The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
- `__pydantic_complete__` (unknown): Whether model building is completed, or if there are still undefined fields.
- `__pydantic_core_schema__` (unknown): The core schema of the model.
- `__pydantic_custom_init__` (unknown): Whether the model has a custom `__init__` function.
- `__pydantic_decorators__` (unknown): Metadata containing the decorators defined on the model.
This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
- `__pydantic_generic_metadata__` (unknown): Metadata for generic models; contains data used for a similar purpose to
__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
- `__pydantic_parent_namespace__` (unknown): Parent namespace of the model, used for automatic rebuilding of models.
- `__pydantic_post_init__` (unknown): The name of the post-init method for the model, if defined.
- `__pydantic_root_model__` (unknown): Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
- `__pydantic_serializer__` (unknown): The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
- `__pydantic_validator__` (unknown): The `pydantic-core` `SchemaValidator` used to validate instances of the model.
- `__pydantic_fields__` (unknown): A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
- `__pydantic_computed_fields__` (unknown): A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
- `__pydantic_extra__` (unknown): A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
is set to `'allow'`.
- `__pydantic_fields_set__` (unknown): The names of fields explicitly set during instantiation.
- `__pydantic_private__` (unknown): Values of private attributes set on the model instance.

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

## Class `ModelResponseMessage`


**Description:**
!!! abstract "Usage Documentation"
[Models](../concepts/models.md)

A base class for creating Pydantic models.

**Parameters:**
- `__class_vars__` (unknown): The names of the class variables defined on the model.
- `__private_attributes__` (unknown): Metadata about the private attributes of the model.
- `__signature__` (unknown): The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
- `__pydantic_complete__` (unknown): Whether model building is completed, or if there are still undefined fields.
- `__pydantic_core_schema__` (unknown): The core schema of the model.
- `__pydantic_custom_init__` (unknown): Whether the model has a custom `__init__` function.
- `__pydantic_decorators__` (unknown): Metadata containing the decorators defined on the model.
This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
- `__pydantic_generic_metadata__` (unknown): Metadata for generic models; contains data used for a similar purpose to
__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
- `__pydantic_parent_namespace__` (unknown): Parent namespace of the model, used for automatic rebuilding of models.
- `__pydantic_post_init__` (unknown): The name of the post-init method for the model, if defined.
- `__pydantic_root_model__` (unknown): Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
- `__pydantic_serializer__` (unknown): The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
- `__pydantic_validator__` (unknown): The `pydantic-core` `SchemaValidator` used to validate instances of the model.
- `__pydantic_fields__` (unknown): A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
- `__pydantic_computed_fields__` (unknown): A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
- `__pydantic_extra__` (unknown): A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
is set to `'allow'`.
- `__pydantic_fields_set__` (unknown): The names of fields explicitly set during instantiation.
- `__pydantic_private__` (unknown): Values of private attributes set on the model instance.

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

## Class `ModelUpdateMessage`


**Description:**
!!! abstract "Usage Documentation"
[Models](../concepts/models.md)

A base class for creating Pydantic models.

**Parameters:**
- `__class_vars__` (unknown): The names of the class variables defined on the model.
- `__private_attributes__` (unknown): Metadata about the private attributes of the model.
- `__signature__` (unknown): The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
- `__pydantic_complete__` (unknown): Whether model building is completed, or if there are still undefined fields.
- `__pydantic_core_schema__` (unknown): The core schema of the model.
- `__pydantic_custom_init__` (unknown): Whether the model has a custom `__init__` function.
- `__pydantic_decorators__` (unknown): Metadata containing the decorators defined on the model.
This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
- `__pydantic_generic_metadata__` (unknown): Metadata for generic models; contains data used for a similar purpose to
__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
- `__pydantic_parent_namespace__` (unknown): Parent namespace of the model, used for automatic rebuilding of models.
- `__pydantic_post_init__` (unknown): The name of the post-init method for the model, if defined.
- `__pydantic_root_model__` (unknown): Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
- `__pydantic_serializer__` (unknown): The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
- `__pydantic_validator__` (unknown): The `pydantic-core` `SchemaValidator` used to validate instances of the model.
- `__pydantic_fields__` (unknown): A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
- `__pydantic_computed_fields__` (unknown): A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
- `__pydantic_extra__` (unknown): A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
is set to `'allow'`.
- `__pydantic_fields_set__` (unknown): The names of fields explicitly set during instantiation.
- `__pydantic_private__` (unknown): Values of private attributes set on the model instance.

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

## Class `ModelUpdateType`


**Description:**
Enum where members are also (and must be) ints
