# mlserver.types.InferenceErrorResponse

<a id="id1"></a>

**Module:** `mlserver.types`
**Class:** `InferenceErrorResponse`

#### NOTE
This page was auto-generated. Edit the docstring of `mlserver.types.InferenceErrorResponse` for content changes.

## Overview

### *class* mlserver.types.InferenceErrorResponse(\*, error: str | None = None)

Bases: `BaseModel`

#### error *: str | None*

#### \_\_init_\_(\*\*data: Any) → None

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

#### *classmethod* construct(\_fields_set: set[str] | None = None, \*\*values: Any) → Self

#### copy(\*, include: AbstractSetIntStr | MappingIntStrAny | None = None, exclude: AbstractSetIntStr | MappingIntStrAny | None = None, update: Dict[str, Any] | None = None, deep: bool = False) → Self

Returns a copy of the model.

!!! warning “Deprecated”
: This method is now deprecated; use model_copy instead.

If you need include or exclude, use:

``py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
``

* **Parameters:**
  * **include** – Optional set or mapping specifying which fields to include in the copied model.
  * **exclude** – Optional set or mapping specifying which fields to exclude in the copied model.
  * **update** – Optional dictionary of field-value pairs to override field values in the copied model.
  * **deep** – If True, the values of fields that are Pydantic models will be deep-copied.
* **Returns:**
  A copy of the model with included, excluded and updated fields as specified.

#### dict(\*, include: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, exclude: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False) → Dict[str, Any]

#### *classmethod* from_orm(obj: Any) → Self

#### json(\*, include: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, exclude: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, encoder: Callable[[Any], Any] | None = PydanticUndefined, models_as_dict: bool = PydanticUndefined, \*\*dumps_kwargs: Any) → str

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### *classmethod* model_construct(\_fields_set: set[str] | None = None, \*\*values: Any) → Self

Creates a new instance of the Model class with validated data.

Creates a new model setting \_\_dict_\_ and \_\_pydantic_fields_set_\_ from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
: model_construct() generally respects the model_config.extra setting on the provided model.
  That is, if model_config.extra == ‘allow’, then all extra passed values are added to the model instance’s \_\_dict_\_
  and \_\_pydantic_extra_\_ fields. If model_config.extra == ‘ignore’ (the default), then all extra passed values are ignored.
  Because no validation is performed with a call to model_construct(), having model_config.extra == ‘forbid’ does not result in
  an error if extra values are passed, but they will be ignored.

* **Parameters:**
  * **\_fields_set** – A set of field names that were originally explicitly set during instantiation. If provided,
    this is directly used for the [model_fields_set][pydantic.BaseModel.model_fields_set] attribute.
    Otherwise, the field names from the values argument will be used.
  * **values** – Trusted or pre-validated data dictionary.
* **Returns:**
  A new instance of the Model class with validated data.

#### model_copy(\*, update: dict[str, Any] | None = None, deep: bool = False) → Self

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy](https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy)

Returns a copy of the model.

* **Parameters:**
  * **update** – Values to change/add in the new model. Note: the data is not validated
    before creating the new model. You should trust this data.
  * **deep** – Set to True to make a deep copy of the model.
* **Returns:**
  New model instance.

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump](https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

* **Parameters:**
  * **mode** – The mode in which to_python should run.
    If mode is ‘json’, the output will only contain JSON serializable types.
    If mode is ‘python’, the output may contain non-JSON-serializable Python objects.
  * **include** – A set of fields to include in the output.
  * **exclude** – A set of fields to exclude from the output.
  * **context** – Additional context to pass to the serializer.
  * **by_alias** – Whether to use the field’s alias in the dictionary key if defined.
  * **exclude_unset** – Whether to exclude fields that have not been explicitly set.
  * **exclude_defaults** – Whether to exclude fields that are set to their default value.
  * **exclude_none** – Whether to exclude fields that have a value of None.
  * **round_trip** – If True, dumped values should be valid as input for non-idempotent types such as Json[T].
  * **warnings** – How to handle serialization errors. False/”none” ignores them, True/”warn” logs errors,
    “error” raises a [PydanticSerializationError][pydantic_core.PydanticSerializationError].
  * **serialize_as_any** – Whether to serialize fields with duck-typing serialization behavior.
* **Returns:**
  A dictionary representation of the model.

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json](https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic’s to_json method.

* **Parameters:**
  * **indent** – Indentation to use in the JSON output. If None is passed, the output will be compact.
  * **include** – Field(s) to include in the JSON output.
  * **exclude** – Field(s) to exclude from the JSON output.
  * **context** – Additional context to pass to the serializer.
  * **by_alias** – Whether to serialize using field aliases.
  * **exclude_unset** – Whether to exclude fields that have not been explicitly set.
  * **exclude_defaults** – Whether to exclude fields that are set to their default value.
  * **exclude_none** – Whether to exclude fields that have a value of None.
  * **round_trip** – If True, dumped values should be valid as input for non-idempotent types such as Json[T].
  * **warnings** – How to handle serialization errors. False/”none” ignores them, True/”warn” logs errors,
    “error” raises a [PydanticSerializationError][pydantic_core.PydanticSerializationError].
  * **serialize_as_any** – Whether to serialize fields with duck-typing serialization behavior.
* **Returns:**
  A JSON string representation of the model.

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'error': FieldInfo(annotation=Union[str, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

#### *classmethod* model_json_schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}', schema_generator: type[pydantic.json_schema.GenerateJsonSchema] = <class 'pydantic.json_schema.GenerateJsonSchema'>, mode: ~typing.Literal['validation', 'serialization'] = 'validation') → dict[str, Any]

Generates a JSON schema for a model class.

* **Parameters:**
  * **by_alias** – Whether to use attribute aliases or not.
  * **ref_template** – The reference template.
  * **schema_generator** – To override the logic used to generate the JSON schema, as a subclass of
    GenerateJsonSchema with your desired modifications
  * **mode** – The mode in which to generate the schema.
* **Returns:**
  The JSON schema for the given model class.

#### *classmethod* model_parametrized_name(params: tuple[type[Any], ...]) → str

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

* **Parameters:**
  **params** – Tuple of types of the class. Given a generic class
  Model with 2 type variables and a concrete model Model[str, int],
  the value (str, int) would be passed to params.
* **Returns:**
  String representing the new class where params are passed to cls as type variables.
* **Raises:**
  **TypeError** – Raised when trying to generate concrete names for non-generic models.

#### model_post_init(\_BaseModel_\_context: Any) → None

Override this method to perform additional initialization after \_\_init_\_ and model_construct.
This is useful if you want to do some validation that requires the entire model to be initialized.

#### *classmethod* model_rebuild(\*, force: bool = False, raise_errors: bool = True, \_parent_namespace_depth: int = 2, \_types_namespace: dict[str, Any] | None = None) → bool | None

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

* **Parameters:**
  * **force** – Whether to force the rebuilding of the model schema, defaults to False.
  * **raise_errors** – Whether to raise errors, defaults to True.
  * **\_parent_namespace_depth** – The depth level of the parent namespace, defaults to 2.
  * **\_types_namespace** – The types namespace, defaults to None.
* **Returns:**
  Returns None if the schema is already “complete” and rebuilding was not required.
  If rebuilding \_was_ required, returns True if rebuilding was successful, otherwise False.

#### *classmethod* model_validate(obj: Any, \*, strict: bool | None = None, from_attributes: bool | None = None, context: Any | None = None) → Self

Validate a pydantic model instance.

* **Parameters:**
  * **obj** – The object to validate.
  * **strict** – Whether to enforce types strictly.
  * **from_attributes** – Whether to extract data from object attributes.
  * **context** – Additional context to pass to the validator.
* **Raises:**
  **ValidationError** – If the object could not be validated.
* **Returns:**
  The validated model instance.

#### *classmethod* model_validate_json(json_data: str | bytes | bytearray, \*, strict: bool | None = None, context: Any | None = None) → Self

Usage docs: [https://docs.pydantic.dev/2.9/concepts/json/#json-parsing](https://docs.pydantic.dev/2.9/concepts/json/#json-parsing)

Validate the given JSON data against the Pydantic model.

* **Parameters:**
  * **json_data** – The JSON data to validate.
  * **strict** – Whether to enforce types strictly.
  * **context** – Extra variables to pass to the validator.
* **Returns:**
  The validated Pydantic model.
* **Raises:**
  **ValidationError** – If json_data is not a JSON string or the object could not be validated.

#### *classmethod* model_validate_strings(obj: Any, \*, strict: bool | None = None, context: Any | None = None) → Self

Validate the given object with string data against the Pydantic model.

* **Parameters:**
  * **obj** – The object containing string data to validate.
  * **strict** – Whether to enforce types strictly.
  * **context** – Extra variables to pass to the validator.
* **Returns:**
  The validated Pydantic model.

#### *classmethod* parse_file(path: str | Path, \*, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False) → Self

#### *classmethod* parse_obj(obj: Any) → Self

#### *classmethod* parse_raw(b: str | bytes, \*, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False) → Self

#### *classmethod* schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}') → Dict[str, Any]

#### *classmethod* schema_json(\*, by_alias: bool = True, ref_template: str = '#/$defs/{model}', \*\*dumps_kwargs: Any) → str

#### *classmethod* update_forward_refs(\*\*localns: Any) → None

#### *classmethod* validate(value: Any) → Self

## Quick Reference

Jump to Methods ·
Jump to Attributes ·
[All Members](#mlserver-types-inferenceerrorresponse-members)

## Signature

### mlserver.types.InferenceErrorResponse.\_\_init_\_

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

## Source Link

### Where did this come from?

If `sphinx.ext.linkcode` is enabled, a “View source” link will appear near the class and members in GitBook.

<!-- All Members -->
<!-- ----------- -->
<!-- .. autosummary:: -->
<!-- :toctree: -->
<!-- :nosignatures: -->
<!-- :template: attribute.rst -->
<!-- __abstractmethods__ -->
<!-- __annotations__ -->
<!-- __class__ -->
<!-- __class_getitem__ -->
<!-- __class_vars__ -->
<!-- __copy__ -->
<!-- __deepcopy__ -->
<!-- __delattr__ -->
<!-- __dict__ -->
<!-- __dir__ -->
<!-- __doc__ -->
<!-- __eq__ -->
<!-- __fields_set__ -->
<!-- __format__ -->
<!-- __ge__ -->
<!-- __get_pydantic_core_schema__ -->
<!-- __get_pydantic_json_schema__ -->
<!-- __getattr__ -->
<!-- __getattribute__ -->
<!-- __getstate__ -->
<!-- __gt__ -->
<!-- __hash__ -->
<!-- __init__ -->
<!-- __init_subclass__ -->
<!-- __iter__ -->
<!-- __le__ -->
<!-- __lt__ -->
<!-- __module__ -->
<!-- __ne__ -->
<!-- __new__ -->
<!-- __pretty__ -->
<!-- __private_attributes__ -->
<!-- __pydantic_complete__ -->
<!-- __pydantic_core_schema__ -->
<!-- __pydantic_custom_init__ -->
<!-- __pydantic_decorators__ -->
<!-- __pydantic_extra__ -->
<!-- __pydantic_fields_set__ -->
<!-- __pydantic_generic_metadata__ -->
<!-- __pydantic_init_subclass__ -->
<!-- __pydantic_parent_namespace__ -->
<!-- __pydantic_post_init__ -->
<!-- __pydantic_private__ -->
<!-- __pydantic_root_model__ -->
<!-- __pydantic_serializer__ -->
<!-- __pydantic_validator__ -->
<!-- __reduce__ -->
<!-- __reduce_ex__ -->
<!-- __repr__ -->
<!-- __repr_args__ -->
<!-- __repr_name__ -->
<!-- __repr_str__ -->
<!-- __rich_repr__ -->
<!-- __setattr__ -->
<!-- __setstate__ -->
<!-- __signature__ -->
<!-- __sizeof__ -->
<!-- __slots__ -->
<!-- __str__ -->
<!-- __subclasshook__ -->
<!-- __weakref__ -->
<!-- _abc_impl -->
<!-- _calculate_keys -->
<!-- _check_frozen -->
<!-- _copy_and_set_values -->
<!-- _get_value -->
<!-- _iter -->
<!-- construct -->
<!-- copy -->
<!-- dict -->
<!-- from_orm -->
<!-- json -->
<!-- model_computed_fields -->
<!-- model_config -->
<!-- model_construct -->
<!-- model_copy -->
<!-- model_dump -->
<!-- model_dump_json -->
<!-- model_extra -->
<!-- model_fields -->
<!-- model_fields_set -->
<!-- model_json_schema -->
<!-- model_parametrized_name -->
<!-- model_post_init -->
<!-- model_rebuild -->
<!-- model_validate -->
<!-- model_validate_json -->
<!-- model_validate_strings -->
<!-- parse_file -->
<!-- parse_obj -->
<!-- parse_raw -->
<!-- schema -->
<!-- schema_json -->
<!-- update_forward_refs -->
<!-- validate -->
<!-- .. _mlserver-types-InferenceErrorResponse-methods: -->
<!-- Methods -->
<!-- ------- -->
<!-- .. autosummary:: -->
<!-- :toctree: -->
<!-- :nosignatures: -->
<!-- :template: method.rst -->
<!-- __init__ -->
<!-- construct -->
<!-- copy -->
<!-- dict -->
<!-- from_orm -->
<!-- json -->
<!-- model_construct -->
<!-- model_copy -->
<!-- model_dump -->
<!-- model_dump_json -->
<!-- model_json_schema -->
<!-- model_parametrized_name -->
<!-- model_post_init -->
<!-- model_rebuild -->
<!-- model_validate -->
<!-- model_validate_json -->
<!-- model_validate_strings -->
<!-- parse_file -->
<!-- parse_obj -->
<!-- parse_raw -->
<!-- schema -->
<!-- schema_json -->
<!-- update_forward_refs -->
<!-- validate -->
<!-- .. _mlserver-types-InferenceErrorResponse-attributes: -->
<!-- Attributes -->
<!-- ---------- -->
<!-- .. autosummary:: -->
<!-- :toctree: -->
<!-- :nosignatures: -->
<!-- :template: attribute.rst -->
<!-- model_computed_fields -->
<!-- model_config -->
<!-- model_extra -->
<!-- model_fields -->
<!-- model_fields_set -->
<!-- error -->
