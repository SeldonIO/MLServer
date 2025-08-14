# Types

### *class* mlserver.types.MetadataServerResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **version** (*str*)
  * **extensions** (*List* *[**str* *]*)

#### name *: str*

#### version *: str*

#### extensions *: List[str]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'extensions': FieldInfo(annotation=List[str], required=True), 'name': FieldInfo(annotation=str, required=True), 'version': FieldInfo(annotation=str, required=True)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.MetadataServerErrorResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  **error** (*str*)

#### error *: str*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'error': FieldInfo(annotation=str, required=True)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.Datatype(value)

Bases: `Enum`

An enumeration.

#### BOOL *= 'BOOL'*

#### UINT8 *= 'UINT8'*

#### UINT16 *= 'UINT16'*

#### UINT32 *= 'UINT32'*

#### UINT64 *= 'UINT64'*

#### INT8 *= 'INT8'*

#### INT16 *= 'INT16'*

#### INT32 *= 'INT32'*

#### INT64 *= 'INT64'*

#### FP16 *= 'FP16'*

#### FP32 *= 'FP32'*

#### FP64 *= 'FP64'*

#### BYTES *= 'BYTES'*

### *class* mlserver.types.MetadataTensor(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **datatype** ([*Datatype*](#mlserver.types.Datatype))
  * **shape** (*List* *[**int* *]*)
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)

#### name *: str*

#### datatype *: Datatype*

#### shape *: List[int]*

#### parameters *: Optional[Parameters]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'datatype': FieldInfo(annotation=Datatype, required=True), 'name': FieldInfo(annotation=str, required=True), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None), 'shape': FieldInfo(annotation=List[int], required=True)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.MetadataModelErrorResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  **error** (*str*)

#### error *: str*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'error': FieldInfo(annotation=str, required=True)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.Parameters(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **content_type** (*str* *|* *None*)
  * **headers** (*Dict* *[**str* *,* *Any* *]*  *|* *None*)
  * **extra_data** (*Any*)

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'allow', 'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### content_type *: Optional[str]*

#### headers *: Optional[Dict[str, Any]]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'content_type': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'headers': FieldInfo(annotation=Union[Dict[str, Any], NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.TensorData(root=PydanticUndefined, \*\*data)

Bases: `RootModel[Union[List, Any]]`

* **Parameters:**
  **root** (*List* *|* *Any*)

#### root *: Union[List, Any]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'root': FieldInfo(annotation=Union[List, Any], required=True, title='TensorData')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.RequestOutput(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)

#### name *: str*

#### parameters *: Optional[Parameters]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'name': FieldInfo(annotation=str, required=True), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.ResponseOutput(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **shape** (*List* *[**int* *]*)
  * **datatype** ([*Datatype*](#mlserver.types.Datatype))
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)
  * **data** ([*TensorData*](#mlserver.types.TensorData))

#### name *: str*

#### shape *: List[int]*

#### datatype *: Datatype*

#### parameters *: Optional[Parameters]*

#### data *: TensorData*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'data': FieldInfo(annotation=TensorData, required=True), 'datatype': FieldInfo(annotation=Datatype, required=True), 'name': FieldInfo(annotation=str, required=True), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None), 'shape': FieldInfo(annotation=List[int], required=True)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.InferenceResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **model_name** (*str*)
  * **model_version** (*str* *|* *None*)
  * **id** (*str* *|* *None*)
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)
  * **outputs** (*List* *[*[*ResponseOutput*](#mlserver.types.ResponseOutput) *]*)

#### model_name *: str*

#### model_version *: Optional[str]*

#### id *: Optional[str]*

#### parameters *: Optional[Parameters]*

#### outputs *: List[ResponseOutput]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'id': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'model_name': FieldInfo(annotation=str, required=True), 'model_version': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'outputs': FieldInfo(annotation=List[mlserver.types.dataplane.ResponseOutput], required=True), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.InferenceErrorResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  **error** (*str* *|* *None*)

#### error *: Optional[str]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'error': FieldInfo(annotation=Union[str, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.MetadataModelResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **versions** (*List* *[**str* *]*  *|* *None*)
  * **platform** (*str*)
  * **inputs** (*List* *[*[*MetadataTensor*](#mlserver.types.MetadataTensor) *]*  *|* *None*)
  * **outputs** (*List* *[*[*MetadataTensor*](#mlserver.types.MetadataTensor) *]*  *|* *None*)
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)

#### name *: str*

#### versions *: Optional[List[str]]*

#### platform *: str*

#### inputs *: Optional[List[MetadataTensor]]*

#### outputs *: Optional[List[MetadataTensor]]*

#### parameters *: Optional[Parameters]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'inputs': FieldInfo(annotation=Union[List[mlserver.types.dataplane.MetadataTensor], NoneType], required=False, default=None), 'name': FieldInfo(annotation=str, required=True), 'outputs': FieldInfo(annotation=Union[List[mlserver.types.dataplane.MetadataTensor], NoneType], required=False, default=None), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None), 'platform': FieldInfo(annotation=str, required=True), 'versions': FieldInfo(annotation=Union[List[str], NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.RequestInput(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **shape** (*List* *[**int* *]*)
  * **datatype** ([*Datatype*](#mlserver.types.Datatype))
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)
  * **data** ([*TensorData*](#mlserver.types.TensorData))

#### name *: str*

#### shape *: List[int]*

#### datatype *: Datatype*

#### parameters *: Optional[Parameters]*

#### data *: TensorData*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'data': FieldInfo(annotation=TensorData, required=True), 'datatype': FieldInfo(annotation=Datatype, required=True), 'name': FieldInfo(annotation=str, required=True), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None), 'shape': FieldInfo(annotation=List[int], required=True)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.InferenceRequest(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **id** (*str* *|* *None*)
  * **parameters** ([*Parameters*](#mlserver.types.Parameters) *|* *None*)
  * **inputs** (*List* *[*[*RequestInput*](#mlserver.types.RequestInput) *]*)
  * **outputs** (*List* *[*[*RequestOutput*](#mlserver.types.RequestOutput) *]*  *|* *None*)

#### id *: Optional[str]*

#### parameters *: Optional[Parameters]*

#### inputs *: List[RequestInput]*

#### outputs *: Optional[List[RequestOutput]]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'id': FieldInfo(annotation=Union[str, NoneType], required=False, default=None), 'inputs': FieldInfo(annotation=List[mlserver.types.dataplane.RequestInput], required=True), 'outputs': FieldInfo(annotation=Union[List[mlserver.types.dataplane.RequestOutput], NoneType], required=False, default=None), 'parameters': FieldInfo(annotation=Union[Parameters, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.RepositoryIndexRequest(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  **ready** (*bool* *|* *None*)

#### ready *: Optional[bool]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'ready': FieldInfo(annotation=Union[bool, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.RepositoryIndexResponseItem(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  * **name** (*str*)
  * **version** (*str* *|* *None*)
  * **state** ([*State*](#mlserver.types.State))
  * **reason** (*str*)

#### name *: str*

#### version *: Optional[str]*

#### state *: State*

#### reason *: str*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'name': FieldInfo(annotation=str, required=True), 'reason': FieldInfo(annotation=str, required=True), 'state': FieldInfo(annotation=State, required=True), 'version': FieldInfo(annotation=Union[str, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.State(value)

Bases: `Enum`

An enumeration.

#### UNKNOWN *= 'UNKNOWN'*

#### READY *= 'READY'*

#### UNAVAILABLE *= 'UNAVAILABLE'*

#### LOADING *= 'LOADING'*

#### UNLOADING *= 'UNLOADING'*

### *class* mlserver.types.RepositoryIndexResponse(root=PydanticUndefined, \*\*data)

Bases: `RepositoryIndexResponseItem]]`

* **Parameters:**
  **root** (*List* *[*[*RepositoryIndexResponseItem*](#mlserver.types.RepositoryIndexResponseItem) *]*)

#### root *: List[RepositoryIndexResponseItem]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'root': FieldInfo(annotation=List[mlserver.types.model_repository.RepositoryIndexResponseItem], required=True, title='RepositoryIndexResponse')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.RepositoryLoadErrorResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  **error** (*str* *|* *None*)

#### error *: Optional[str]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'error': FieldInfo(annotation=Union[str, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* mlserver.types.RepositoryUnloadErrorResponse(\*\*data)

Bases: `BaseModel`

* **Parameters:**
  **error** (*str* *|* *None*)

#### error *: Optional[str]*

#### model_computed_fields *: ClassVar[Dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'protected_namespaces': (), 'use_enum_values': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[Dict[str, FieldInfo]]* *= {'error': FieldInfo(annotation=Union[str, NoneType], required=False, default=None)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo] objects.

This replaces Model._\_fields_\_ from Pydantic V1.
