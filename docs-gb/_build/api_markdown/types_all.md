### *class* mlserver.types.Datatype(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

#### BOOL *= 'BOOL'*

#### BYTES *= 'BYTES'*

#### FP16 *= 'FP16'*

#### FP32 *= 'FP32'*

#### FP64 *= 'FP64'*

#### INT16 *= 'INT16'*

#### INT32 *= 'INT32'*

#### INT64 *= 'INT64'*

#### INT8 *= 'INT8'*

#### UINT16 *= 'UINT16'*

#### UINT32 *= 'UINT32'*

#### UINT64 *= 'UINT64'*

#### UINT8 *= 'UINT8'*

### *pydantic model* mlserver.types.InferenceErrorResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "InferenceErrorResponse",
   "type": "object",
   "properties": {
      "error": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Error"
      }
   }
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.InferenceRequest

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "InferenceRequest",
   "type": "object",
   "properties": {
      "id": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Id"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      },
      "inputs": {
         "items": {
            "$ref": "#/$defs/RequestInput"
         },
         "title": "Inputs",
         "type": "array"
      },
      "outputs": {
         "anyOf": [
            {
               "items": {
                  "$ref": "#/$defs/RequestOutput"
               },
               "type": "array"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Outputs"
      }
   },
   "$defs": {
      "Datatype": {
         "enum": [
            "BOOL",
            "UINT8",
            "UINT16",
            "UINT32",
            "UINT64",
            "INT8",
            "INT16",
            "INT32",
            "INT64",
            "FP16",
            "FP32",
            "FP64",
            "BYTES"
         ],
         "title": "Datatype",
         "type": "string"
      },
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      },
      "RequestInput": {
         "properties": {
            "name": {
               "title": "Name",
               "type": "string"
            },
            "shape": {
               "items": {
                  "type": "integer"
               },
               "title": "Shape",
               "type": "array"
            },
            "datatype": {
               "$ref": "#/$defs/Datatype"
            },
            "parameters": {
               "anyOf": [
                  {
                     "$ref": "#/$defs/Parameters"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null
            },
            "data": {
               "$ref": "#/$defs/TensorData"
            }
         },
         "required": [
            "name",
            "shape",
            "datatype",
            "data"
         ],
         "title": "RequestInput",
         "type": "object"
      },
      "RequestOutput": {
         "properties": {
            "name": {
               "title": "Name",
               "type": "string"
            },
            "parameters": {
               "anyOf": [
                  {
                     "$ref": "#/$defs/Parameters"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null
            }
         },
         "required": [
            "name"
         ],
         "title": "RequestOutput",
         "type": "object"
      },
      "TensorData": {
         "anyOf": [
            {
               "items": {},
               "type": "array"
            },
            {}
         ],
         "title": "TensorData"
      }
   },
   "required": [
      "inputs"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `id (str | None)`
  - `inputs (List[mlserver.types.dataplane.RequestInput])`
  - `outputs (List[mlserver.types.dataplane.RequestOutput] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* id *: str | None* *= None*

#### *field* inputs *: List[RequestInput]* *[Required]*

#### *field* outputs *: List[RequestOutput] | None* *= None*

#### *field* parameters *: Parameters | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.InferenceResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "InferenceResponse",
   "type": "object",
   "properties": {
      "model_name": {
         "title": "Model Name",
         "type": "string"
      },
      "model_version": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Model Version"
      },
      "id": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Id"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      },
      "outputs": {
         "items": {
            "$ref": "#/$defs/ResponseOutput"
         },
         "title": "Outputs",
         "type": "array"
      }
   },
   "$defs": {
      "Datatype": {
         "enum": [
            "BOOL",
            "UINT8",
            "UINT16",
            "UINT32",
            "UINT64",
            "INT8",
            "INT16",
            "INT32",
            "INT64",
            "FP16",
            "FP32",
            "FP64",
            "BYTES"
         ],
         "title": "Datatype",
         "type": "string"
      },
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      },
      "ResponseOutput": {
         "properties": {
            "name": {
               "title": "Name",
               "type": "string"
            },
            "shape": {
               "items": {
                  "type": "integer"
               },
               "title": "Shape",
               "type": "array"
            },
            "datatype": {
               "$ref": "#/$defs/Datatype"
            },
            "parameters": {
               "anyOf": [
                  {
                     "$ref": "#/$defs/Parameters"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null
            },
            "data": {
               "$ref": "#/$defs/TensorData"
            }
         },
         "required": [
            "name",
            "shape",
            "datatype",
            "data"
         ],
         "title": "ResponseOutput",
         "type": "object"
      },
      "TensorData": {
         "anyOf": [
            {
               "items": {},
               "type": "array"
            },
            {}
         ],
         "title": "TensorData"
      }
   },
   "required": [
      "model_name",
      "outputs"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `id (str | None)`
  - `model_name (str)`
  - `model_version (str | None)`
  - `outputs (List[mlserver.types.dataplane.ResponseOutput])`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* id *: str | None* *= None*

#### *field* model_name *: str* *[Required]*

#### *field* model_version *: str | None* *= None*

#### *field* outputs *: List[ResponseOutput]* *[Required]*

#### *field* parameters *: Parameters | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.MetadataModelErrorResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "MetadataModelErrorResponse",
   "type": "object",
   "properties": {
      "error": {
         "title": "Error",
         "type": "string"
      }
   },
   "required": [
      "error"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `error (str)`

#### *field* error *: str* *[Required]*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.MetadataModelResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "MetadataModelResponse",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "versions": {
         "anyOf": [
            {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Versions"
      },
      "platform": {
         "title": "Platform",
         "type": "string"
      },
      "inputs": {
         "anyOf": [
            {
               "items": {
                  "$ref": "#/$defs/MetadataTensor"
               },
               "type": "array"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Inputs"
      },
      "outputs": {
         "anyOf": [
            {
               "items": {
                  "$ref": "#/$defs/MetadataTensor"
               },
               "type": "array"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Outputs"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      }
   },
   "$defs": {
      "Datatype": {
         "enum": [
            "BOOL",
            "UINT8",
            "UINT16",
            "UINT32",
            "UINT64",
            "INT8",
            "INT16",
            "INT32",
            "INT64",
            "FP16",
            "FP32",
            "FP64",
            "BYTES"
         ],
         "title": "Datatype",
         "type": "string"
      },
      "MetadataTensor": {
         "properties": {
            "name": {
               "title": "Name",
               "type": "string"
            },
            "datatype": {
               "$ref": "#/$defs/Datatype"
            },
            "shape": {
               "items": {
                  "type": "integer"
               },
               "title": "Shape",
               "type": "array"
            },
            "parameters": {
               "anyOf": [
                  {
                     "$ref": "#/$defs/Parameters"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null
            }
         },
         "required": [
            "name",
            "datatype",
            "shape"
         ],
         "title": "MetadataTensor",
         "type": "object"
      },
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      }
   },
   "required": [
      "name",
      "platform"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `inputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `name (str)`
  - `outputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `platform (str)`
  - `versions (List[str] | None)`

#### *field* inputs *: List[MetadataTensor] | None* *= None*

#### *field* name *: str* *[Required]*

#### *field* outputs *: List[MetadataTensor] | None* *= None*

#### *field* parameters *: Parameters | None* *= None*

#### *field* platform *: str* *[Required]*

#### *field* versions *: List[str] | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.MetadataServerErrorResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "MetadataServerErrorResponse",
   "type": "object",
   "properties": {
      "error": {
         "title": "Error",
         "type": "string"
      }
   },
   "required": [
      "error"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `error (str)`

#### *field* error *: str* *[Required]*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.MetadataServerResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "MetadataServerResponse",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "version": {
         "title": "Version",
         "type": "string"
      },
      "extensions": {
         "items": {
            "type": "string"
         },
         "title": "Extensions",
         "type": "array"
      }
   },
   "required": [
      "name",
      "version",
      "extensions"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `extensions (List[str])`
  - `name (str)`
  - `version (str)`

#### *field* extensions *: List[str]* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* version *: str* *[Required]*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.MetadataTensor

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "MetadataTensor",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "datatype": {
         "$ref": "#/$defs/Datatype"
      },
      "shape": {
         "items": {
            "type": "integer"
         },
         "title": "Shape",
         "type": "array"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      }
   },
   "$defs": {
      "Datatype": {
         "enum": [
            "BOOL",
            "UINT8",
            "UINT16",
            "UINT32",
            "UINT64",
            "INT8",
            "INT16",
            "INT32",
            "INT64",
            "FP16",
            "FP32",
            "FP64",
            "BYTES"
         ],
         "title": "Datatype",
         "type": "string"
      },
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      }
   },
   "required": [
      "name",
      "datatype",
      "shape"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

#### *field* datatype *: Datatype* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* parameters *: Parameters | None* *= None*

#### *field* shape *: List[int]* *[Required]*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.Parameters

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "Parameters",
   "type": "object",
   "properties": {
      "content_type": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Content Type"
      },
      "headers": {
         "anyOf": [
            {
               "type": "object"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Headers"
      }
   },
   "additionalProperties": true
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
  - **extra**: *str = allow*
* **Fields:**
  - `content_type (str | None)`
  - `headers (Dict[str, Any] | None)`

#### *field* content_type *: str | None* *= None*

#### *field* headers *: Dict[str, Any] | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RepositoryIndexRequest

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RepositoryIndexRequest",
   "type": "object",
   "properties": {
      "ready": {
         "anyOf": [
            {
               "type": "boolean"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Ready"
      }
   }
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `ready (bool | None)`

#### *field* ready *: bool | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RepositoryIndexResponse

Bases: `RootModel[List[RepositoryIndexResponseItem]]`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RepositoryIndexResponse",
   "type": "array",
   "$defs": {
      "RepositoryIndexResponseItem": {
         "properties": {
            "name": {
               "title": "Name",
               "type": "string"
            },
            "version": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Version"
            },
            "state": {
               "$ref": "#/$defs/State"
            },
            "reason": {
               "title": "Reason",
               "type": "string"
            }
         },
         "required": [
            "name",
            "state",
            "reason"
         ],
         "title": "RepositoryIndexResponseItem",
         "type": "object"
      },
      "State": {
         "enum": [
            "UNKNOWN",
            "READY",
            "UNAVAILABLE",
            "LOADING",
            "UNLOADING"
         ],
         "title": "State",
         "type": "string"
      }
   },
   "items": {
      "$ref": "#/$defs/RepositoryIndexResponseItem"
   }
}
```

</details></p>
* **Fields:**
  - `root (List[mlserver.types.model_repository.RepositoryIndexResponseItem])`

#### *field* root *: List[RepositoryIndexResponseItem]* *[Required]*

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

#### *classmethod* model_construct(root: RootModelRootType, \_fields_set: set[str] | None = None) → Self

Create a new model using the provided root object and update fields set.

* **Parameters:**
  * **root** – The root object of the model.
  * **\_fields_set** – The set of fields to be updated.
* **Returns:**
  The new model.
* **Raises:**
  **NotImplemented** – If the model is not a subclass of RootModel.

#### model_copy(\*, update: dict[str, Any] | None = None, deep: bool = False) → Self

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy](https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy)

Returns a copy of the model.

* **Parameters:**
  * **update** – Values to change/add in the new model. Note: the data is not validated
    before creating the new model. You should trust this data.
  * **deep** – Set to True to make a deep copy of the model.
* **Returns:**
  New model instance.

#### model_dump(\*, mode: Literal['json', 'python'] | str = 'python', include: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, exclude: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, context: Any | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, serialize_as_any: bool = False) → dict[str, Any]

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

#### model_dump_json(\*, indent: int | None = None, include: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, exclude: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, context: Any | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, serialize_as_any: bool = False) → str

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RepositoryIndexResponseItem

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RepositoryIndexResponseItem",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "version": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Version"
      },
      "state": {
         "$ref": "#/$defs/State"
      },
      "reason": {
         "title": "Reason",
         "type": "string"
      }
   },
   "$defs": {
      "State": {
         "enum": [
            "UNKNOWN",
            "READY",
            "UNAVAILABLE",
            "LOADING",
            "UNLOADING"
         ],
         "title": "State",
         "type": "string"
      }
   },
   "required": [
      "name",
      "state",
      "reason"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `name (str)`
  - `reason (str)`
  - `state (mlserver.types.model_repository.State)`
  - `version (str | None)`

#### *field* name *: str* *[Required]*

#### *field* reason *: str* *[Required]*

#### *field* state *: State* *[Required]*

#### *field* version *: str | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RepositoryLoadErrorResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RepositoryLoadErrorResponse",
   "type": "object",
   "properties": {
      "error": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Error"
      }
   }
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RepositoryUnloadErrorResponse

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RepositoryUnloadErrorResponse",
   "type": "object",
   "properties": {
      "error": {
         "anyOf": [
            {
               "type": "string"
            },
            {
               "type": "null"
            }
         ],
         "default": null,
         "title": "Error"
      }
   }
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RequestInput

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RequestInput",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "shape": {
         "items": {
            "type": "integer"
         },
         "title": "Shape",
         "type": "array"
      },
      "datatype": {
         "$ref": "#/$defs/Datatype"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      },
      "data": {
         "$ref": "#/$defs/TensorData"
      }
   },
   "$defs": {
      "Datatype": {
         "enum": [
            "BOOL",
            "UINT8",
            "UINT16",
            "UINT32",
            "UINT64",
            "INT8",
            "INT16",
            "INT32",
            "INT64",
            "FP16",
            "FP32",
            "FP64",
            "BYTES"
         ],
         "title": "Datatype",
         "type": "string"
      },
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      },
      "TensorData": {
         "anyOf": [
            {
               "items": {},
               "type": "array"
            },
            {}
         ],
         "title": "TensorData"
      }
   },
   "required": [
      "name",
      "shape",
      "datatype",
      "data"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

#### *field* data *: TensorData* *[Required]*

#### *field* datatype *: Datatype* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* parameters *: Parameters | None* *= None*

#### *field* shape *: List[int]* *[Required]*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.RequestOutput

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "RequestOutput",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      }
   },
   "$defs": {
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      }
   },
   "required": [
      "name"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* name *: str* *[Required]*

#### *field* parameters *: Parameters | None* *= None*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *pydantic model* mlserver.types.ResponseOutput

Bases: `BaseModel`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "ResponseOutput",
   "type": "object",
   "properties": {
      "name": {
         "title": "Name",
         "type": "string"
      },
      "shape": {
         "items": {
            "type": "integer"
         },
         "title": "Shape",
         "type": "array"
      },
      "datatype": {
         "$ref": "#/$defs/Datatype"
      },
      "parameters": {
         "anyOf": [
            {
               "$ref": "#/$defs/Parameters"
            },
            {
               "type": "null"
            }
         ],
         "default": null
      },
      "data": {
         "$ref": "#/$defs/TensorData"
      }
   },
   "$defs": {
      "Datatype": {
         "enum": [
            "BOOL",
            "UINT8",
            "UINT16",
            "UINT32",
            "UINT64",
            "INT8",
            "INT16",
            "INT32",
            "INT64",
            "FP16",
            "FP32",
            "FP64",
            "BYTES"
         ],
         "title": "Datatype",
         "type": "string"
      },
      "Parameters": {
         "additionalProperties": true,
         "properties": {
            "content_type": {
               "anyOf": [
                  {
                     "type": "string"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Content Type"
            },
            "headers": {
               "anyOf": [
                  {
                     "type": "object"
                  },
                  {
                     "type": "null"
                  }
               ],
               "default": null,
               "title": "Headers"
            }
         },
         "title": "Parameters",
         "type": "object"
      },
      "TensorData": {
         "anyOf": [
            {
               "items": {},
               "type": "array"
            },
            {}
         ],
         "title": "TensorData"
      }
   },
   "required": [
      "name",
      "shape",
      "datatype",
      "data"
   ]
}
```

</details></p>
* **Config:**
  - **protected_namespaces**: *tuple = ()*
  - **use_enum_values**: *bool = True*
* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

#### *field* data *: TensorData* *[Required]*

#### *field* datatype *: Datatype* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* parameters *: Parameters | None* *= None*

#### *field* shape *: List[int]* *[Required]*

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *class* mlserver.types.State(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

#### LOADING *= 'LOADING'*

#### READY *= 'READY'*

#### UNAVAILABLE *= 'UNAVAILABLE'*

#### UNKNOWN *= 'UNKNOWN'*

#### UNLOADING *= 'UNLOADING'*

### *pydantic model* mlserver.types.TensorData

Bases: `RootModel[Union[List, Any]]`

<p><details  class="autodoc_pydantic_collapsable_json">
<summary>Show JSON schema</summary>
```json
{
   "title": "TensorData",
   "anyOf": [
      {
         "items": {},
         "type": "array"
      },
      {}
   ]
}
```

</details></p>
* **Fields:**
  - `root (List | Any)`

#### *field* root *: List | Any* *[Required]*

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

#### *classmethod* model_construct(root: RootModelRootType, \_fields_set: set[str] | None = None) → Self

Create a new model using the provided root object and update fields set.

* **Parameters:**
  * **root** – The root object of the model.
  * **\_fields_set** – The set of fields to be updated.
* **Returns:**
  The new model.
* **Raises:**
  **NotImplemented** – If the model is not a subclass of RootModel.

#### model_copy(\*, update: dict[str, Any] | None = None, deep: bool = False) → Self

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy](https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy)

Returns a copy of the model.

* **Parameters:**
  * **update** – Values to change/add in the new model. Note: the data is not validated
    before creating the new model. You should trust this data.
  * **deep** – Set to True to make a deep copy of the model.
* **Returns:**
  New model instance.

#### model_dump(\*, mode: Literal['json', 'python'] | str = 'python', include: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, exclude: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, context: Any | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, serialize_as_any: bool = False) → dict[str, Any]

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

#### model_dump_json(\*, indent: int | None = None, include: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, exclude: Set[int] | Set[str] | Mapping[int, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | Mapping[str, Set[int] | Set[str] | Mapping[int, IncEx | Literal[True]] | Mapping[str, IncEx | Literal[True]] | Literal[True]] | None = None, context: Any | None = None, by_alias: bool = False, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool | Literal['none', 'warn', 'error'] = True, serialize_as_any: bool = False) → str

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

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

### *class* mlserver.types.InferenceRequest(\*, id: str | None = None, parameters: Parameters | None = None, inputs: List[RequestInput], outputs: List[RequestOutput] | None = None)

Bases: `BaseModel`

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

#### *field* id *: str | None* *= None*

#### *field* inputs *: List[RequestInput]* *[Required]*

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

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'id': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'inputs': FieldInfo(annotation=List[RequestInput], required=True), 'outputs': FieldInfo(annotation=Union[List[RequestOutput], NoneType], required=False, default=None), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None)}*

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

#### *field* outputs *: List[RequestOutput] | None* *= None*

#### *field* parameters *: Parameters | None* *= None*

#### *classmethod* parse_file(path: str | Path, \*, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False) → Self

#### *classmethod* parse_obj(obj: Any) → Self

#### *classmethod* parse_raw(b: str | bytes, \*, content_type: str | None = None, encoding: str = 'utf8', proto: DeprecatedParseProtocol | None = None, allow_pickle: bool = False) → Self

#### *classmethod* schema(by_alias: bool = True, ref_template: str = '#/$defs/{model}') → Dict[str, Any]

#### *classmethod* schema_json(\*, by_alias: bool = True, ref_template: str = '#/$defs/{model}', \*\*dumps_kwargs: Any) → str

#### *classmethod* update_forward_refs(\*\*localns: Any) → None

#### *classmethod* validate(value: Any) → Self

### *class* mlserver.types.InferenceErrorResponse(\*, error: str | None = None)

Bases: `BaseModel`

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

#### *field* error *: str | None* *= None*

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
