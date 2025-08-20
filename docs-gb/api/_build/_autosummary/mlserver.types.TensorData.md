# TensorData

**Qualified name:** `mlserver.types.TensorData`

## Overview

### *class* mlserver.types.TensorData

Bases: `RootModel[Union[List, Any]]`

#### root *: List | Any*

#### \_\_init_\_(root=PydanticUndefined, \*\*data)

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

* **Parameters:**
  **root** (*RootModelRootType*) – 
* **Return type:**
  *None*

#### *classmethod* construct(\_fields_set=None, \*\*values)

* **Parameters:**
  * **\_fields_set** (*set* *[**str* *]*  *|* *None*) – 
  * **values** (*Any*) – 
* **Return type:**
  *Self*

#### copy(\*, include=None, exclude=None, update=None, deep=False)

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
  * **include** (*AbstractSetIntStr* *|* *MappingIntStrAny* *|* *None*) – Optional set or mapping specifying which fields to include in the copied model.
  * **exclude** (*AbstractSetIntStr* *|* *MappingIntStrAny* *|* *None*) – Optional set or mapping specifying which fields to exclude in the copied model.
  * **update** (*Dict* *[**str* *,* *Any* *]*  *|* *None*) – Optional dictionary of field-value pairs to override field values in the copied model.
  * **deep** (*bool*) – If True, the values of fields that are Pydantic models will be deep-copied.
* **Returns:**
  A copy of the model with included, excluded and updated fields as specified.
* **Return type:**
  *Self*

#### dict(\*, include=None, exclude=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False)

* **Parameters:**
  * **include** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – 
  * **exclude** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – 
  * **by_alias** (*bool*) – 
  * **exclude_unset** (*bool*) – 
  * **exclude_defaults** (*bool*) – 
  * **exclude_none** (*bool*) – 
* **Return type:**
  *Dict*[*str*, *Any*]

#### *classmethod* from_orm(obj)

* **Parameters:**
  **obj** (*Any*) – 
* **Return type:**
  *Self*

#### json(\*, include=None, exclude=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False, encoder=PydanticUndefined, models_as_dict=PydanticUndefined, \*\*dumps_kwargs)

* **Parameters:**
  * **include** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – 
  * **exclude** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – 
  * **by_alias** (*bool*) – 
  * **exclude_unset** (*bool*) – 
  * **exclude_defaults** (*bool*) – 
  * **exclude_none** (*bool*) – 
  * **encoder** (*Callable* *[* *[**Any* *]* *,* *Any* *]*  *|* *None*) – 
  * **models_as_dict** (*bool*) – 
  * **dumps_kwargs** (*Any*) – 
* **Return type:**
  *str*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### *classmethod* model_construct(root, \_fields_set=None)

Create a new model using the provided root object and update fields set.

* **Parameters:**
  * **root** (*RootModelRootType*) – The root object of the model.
  * **\_fields_set** (*set* *[**str* *]*  *|* *None*) – The set of fields to be updated.
* **Returns:**
  The new model.
* **Raises:**
  **NotImplemented** – If the model is not a subclass of RootModel.
* **Return type:**
  *Self*

#### model_copy(\*, update=None, deep=False)

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy](https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy)

Returns a copy of the model.

* **Parameters:**
  * **update** (*dict* *[**str* *,* *Any* *]*  *|* *None*) – Values to change/add in the new model. Note: the data is not validated
    before creating the new model. You should trust this data.
  * **deep** (*bool*) – Set to True to make a deep copy of the model.
* **Returns:**
  New model instance.
* **Return type:**
  *Self*

#### model_dump(\*, mode='python', include=None, exclude=None, context=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False, round_trip=False, warnings=True, serialize_as_any=False)

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump](https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

* **Parameters:**
  * **mode** (*Literal* *[* *'json'* *,*  *'python'* *]*  *|* *str*) – The mode in which to_python should run.
    If mode is ‘json’, the output will only contain JSON serializable types.
    If mode is ‘python’, the output may contain non-JSON-serializable Python objects.
  * **include** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – A set of fields to include in the output.
  * **exclude** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – A set of fields to exclude from the output.
  * **context** (*Any* *|* *None*) – Additional context to pass to the serializer.
  * **by_alias** (*bool*) – Whether to use the field’s alias in the dictionary key if defined.
  * **exclude_unset** (*bool*) – Whether to exclude fields that have not been explicitly set.
  * **exclude_defaults** (*bool*) – Whether to exclude fields that are set to their default value.
  * **exclude_none** (*bool*) – Whether to exclude fields that have a value of None.
  * **round_trip** (*bool*) – If True, dumped values should be valid as input for non-idempotent types such as Json[T].
  * **warnings** (*bool* *|* *Literal* *[* *'none'* *,*  *'warn'* *,*  *'error'* *]*) – How to handle serialization errors. False/”none” ignores them, True/”warn” logs errors,
    “error” raises a [PydanticSerializationError][pydantic_core.PydanticSerializationError].
  * **serialize_as_any** (*bool*) – Whether to serialize fields with duck-typing serialization behavior.
* **Returns:**
  A dictionary representation of the model.
* **Return type:**
  *dict*[*str*, *Any*]

#### model_dump_json(\*, indent=None, include=None, exclude=None, context=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False, round_trip=False, warnings=True, serialize_as_any=False)

Usage docs: [https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json](https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json)

Generates a JSON representation of the model using Pydantic’s to_json method.

* **Parameters:**
  * **indent** (*int* *|* *None*) – Indentation to use in the JSON output. If None is passed, the output will be compact.
  * **include** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – Field(s) to include in the JSON output.
  * **exclude** (*Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *Set* *[**int* *]*  *|* *Set* *[**str* *]*  *|* *Mapping* *[**int* *,* *IncEx* *|* *Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,*  *~typing.Set* *[**int* *]*  *|*  *~typing.Set* *[**str* *]*  *|*  *~typing.Mapping* *[**int* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Mapping* *[**str* *,* *IncEx* *|*  *~typing.Literal* *[**True* *]* *]*  *|*  *~typing.Literal* *[**True* *]* *]*  *|* *None*) – Field(s) to exclude from the JSON output.
  * **context** (*Any* *|* *None*) – Additional context to pass to the serializer.
  * **by_alias** (*bool*) – Whether to serialize using field aliases.
  * **exclude_unset** (*bool*) – Whether to exclude fields that have not been explicitly set.
  * **exclude_defaults** (*bool*) – Whether to exclude fields that are set to their default value.
  * **exclude_none** (*bool*) – Whether to exclude fields that have a value of None.
  * **round_trip** (*bool*) – If True, dumped values should be valid as input for non-idempotent types such as Json[T].
  * **warnings** (*bool* *|* *Literal* *[* *'none'* *,*  *'warn'* *,*  *'error'* *]*) – How to handle serialization errors. False/”none” ignores them, True/”warn” logs errors,
    “error” raises a [PydanticSerializationError][pydantic_core.PydanticSerializationError].
  * **serialize_as_any** (*bool*) – Whether to serialize fields with duck-typing serialization behavior.
* **Returns:**
  A JSON string representation of the model.
* **Return type:**
  *str*

#### *property* model_extra *: dict[str, Any] | None*

Get extra fields set during validation.

* **Returns:**
  A dictionary of extra fields, or None if config.extra is not set to “allow”.

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'root': FieldInfo(annotation=Union[List, Any], required=True, title='TensorData')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

#### *property* model_fields_set *: set[str]*

Returns the set of fields that have been explicitly set on this model instance.

* **Returns:**
  A set of strings representing the fields that have been set,
  : i.e. that were not filled from defaults.

#### *classmethod* model_json_schema(by_alias=True, ref_template='#/$defs/{model}', schema_generator=<class 'pydantic.json_schema.GenerateJsonSchema'>, mode='validation')

Generates a JSON schema for a model class.

* **Parameters:**
  * **by_alias** (*bool*) – Whether to use attribute aliases or not.
  * **ref_template** (*str*) – The reference template.
  * **schema_generator** (*type* *[**pydantic.json_schema.GenerateJsonSchema* *]*) – To override the logic used to generate the JSON schema, as a subclass of
    GenerateJsonSchema with your desired modifications
  * **mode** (*Literal* *[* *'validation'* *,*  *'serialization'* *]*) – The mode in which to generate the schema.
* **Returns:**
  The JSON schema for the given model class.
* **Return type:**
  *dict*[*str*, *Any*]

#### *classmethod* model_parametrized_name(params)

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

* **Parameters:**
  **params** (*tuple* *[**type* *[**Any* *]* *,*  *...* *]*) – Tuple of types of the class. Given a generic class
  Model with 2 type variables and a concrete model Model[str, int],
  the value (str, int) would be passed to params.
* **Returns:**
  String representing the new class where params are passed to cls as type variables.
* **Raises:**
  **TypeError** – Raised when trying to generate concrete names for non-generic models.
* **Return type:**
  *str*

#### model_post_init(\_BaseModel_\_context)

Override this method to perform additional initialization after \_\_init_\_ and model_construct.
This is useful if you want to do some validation that requires the entire model to be initialized.

* **Parameters:**
  **\_BaseModel_\_context** (*Any*) – 
* **Return type:**
  *None*

#### *classmethod* model_rebuild(\*, force=False, raise_errors=True, \_parent_namespace_depth=2, \_types_namespace=None)

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

* **Parameters:**
  * **force** (*bool*) – Whether to force the rebuilding of the model schema, defaults to False.
  * **raise_errors** (*bool*) – Whether to raise errors, defaults to True.
  * **\_parent_namespace_depth** (*int*) – The depth level of the parent namespace, defaults to 2.
  * **\_types_namespace** (*dict* *[**str* *,* *Any* *]*  *|* *None*) – The types namespace, defaults to None.
* **Returns:**
  Returns None if the schema is already “complete” and rebuilding was not required.
  If rebuilding \_was_ required, returns True if rebuilding was successful, otherwise False.
* **Return type:**
  *bool* | *None*

#### *classmethod* model_validate(obj, \*, strict=None, from_attributes=None, context=None)

Validate a pydantic model instance.

* **Parameters:**
  * **obj** (*Any*) – The object to validate.
  * **strict** (*bool* *|* *None*) – Whether to enforce types strictly.
  * **from_attributes** (*bool* *|* *None*) – Whether to extract data from object attributes.
  * **context** (*Any* *|* *None*) – Additional context to pass to the validator.
* **Raises:**
  **ValidationError** – If the object could not be validated.
* **Returns:**
  The validated model instance.
* **Return type:**
  *Self*

#### *classmethod* model_validate_json(json_data, \*, strict=None, context=None)

Usage docs: [https://docs.pydantic.dev/2.9/concepts/json/#json-parsing](https://docs.pydantic.dev/2.9/concepts/json/#json-parsing)

Validate the given JSON data against the Pydantic model.

* **Parameters:**
  * **json_data** (*str* *|* *bytes* *|* *bytearray*) – The JSON data to validate.
  * **strict** (*bool* *|* *None*) – Whether to enforce types strictly.
  * **context** (*Any* *|* *None*) – Extra variables to pass to the validator.
* **Returns:**
  The validated Pydantic model.
* **Raises:**
  **ValidationError** – If json_data is not a JSON string or the object could not be validated.
* **Return type:**
  *Self*

#### *classmethod* model_validate_strings(obj, \*, strict=None, context=None)

Validate the given object with string data against the Pydantic model.

* **Parameters:**
  * **obj** (*Any*) – The object containing string data to validate.
  * **strict** (*bool* *|* *None*) – Whether to enforce types strictly.
  * **context** (*Any* *|* *None*) – Extra variables to pass to the validator.
* **Returns:**
  The validated Pydantic model.
* **Return type:**
  *Self*

#### *classmethod* parse_file(path, \*, content_type=None, encoding='utf8', proto=None, allow_pickle=False)

* **Parameters:**
  * **path** (*str* *|* *Path*) – 
  * **content_type** (*str* *|* *None*) – 
  * **encoding** (*str*) – 
  * **proto** (*DeprecatedParseProtocol* *|* *None*) – 
  * **allow_pickle** (*bool*) – 
* **Return type:**
  *Self*

#### *classmethod* parse_obj(obj)

* **Parameters:**
  **obj** (*Any*) – 
* **Return type:**
  *Self*

#### *classmethod* parse_raw(b, \*, content_type=None, encoding='utf8', proto=None, allow_pickle=False)

* **Parameters:**
  * **b** (*str* *|* *bytes*) – 
  * **content_type** (*str* *|* *None*) – 
  * **encoding** (*str*) – 
  * **proto** (*DeprecatedParseProtocol* *|* *None*) – 
  * **allow_pickle** (*bool*) – 
* **Return type:**
  *Self*

#### *classmethod* schema(by_alias=True, ref_template='#/$defs/{model}')

* **Parameters:**
  * **by_alias** (*bool*) – 
  * **ref_template** (*str*) – 
* **Return type:**
  *Dict*[*str*, *Any*]

#### *classmethod* schema_json(\*, by_alias=True, ref_template='#/$defs/{model}', \*\*dumps_kwargs)

* **Parameters:**
  * **by_alias** (*bool*) – 
  * **ref_template** (*str*) – 
  * **dumps_kwargs** (*Any*) – 
* **Return type:**
  *str*

#### *classmethod* update_forward_refs(\*\*localns)

* **Parameters:**
  **localns** (*Any*) – 
* **Return type:**
  *None*

#### *classmethod* validate(value)

* **Parameters:**
  **value** (*Any*) – 
* **Return type:**
  *Self*

## Constructor

#### TensorData.\_\_init_\_(root=PydanticUndefined, \*\*data)

Create a new model by parsing and validating input data from keyword arguments.

Raises [ValidationError][pydantic_core.ValidationError] if the input data cannot be
validated to form a valid model.

self is explicitly positional-only to allow self as a field name.

* **Parameters:**
  **root** (*RootModelRootType*) – 
* **Return type:**
  *None*
