<a id="module-mlserver.types"></a>

<a id="types"></a>

# Types

<a id="mlserver.types.MetadataServerResponse"></a>

### *pydantic model* mlserver.types.MetadataServerResponse

Bases: `BaseModel`

* **Fields:**
  - `extensions (List[str])`
  - `name (str)`
  - `version (str)`

<a id="mlserver.types.MetadataServerResponse.extensions"></a>

#### *field* extensions *: List[str]* *[Required]*

<a id="mlserver.types.MetadataServerResponse.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.MetadataServerResponse.version"></a>

#### *field* version *: str* *[Required]*

<a id="mlserver.types.MetadataServerErrorResponse"></a>

### *pydantic model* mlserver.types.MetadataServerErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str)`

<a id="mlserver.types.MetadataServerErrorResponse.error"></a>

#### *field* error *: str* *[Required]*

<a id="mlserver.types.Datatype"></a>

### *class* mlserver.types.Datatype

Bases: `Enum`

<a id="mlserver.types.Datatype.BOOL"></a>

#### BOOL *= 'BOOL'*

<a id="mlserver.types.Datatype.UINT8"></a>

#### UINT8 *= 'UINT8'*

<a id="mlserver.types.Datatype.UINT16"></a>

#### UINT16 *= 'UINT16'*

<a id="mlserver.types.Datatype.UINT32"></a>

#### UINT32 *= 'UINT32'*

<a id="mlserver.types.Datatype.UINT64"></a>

#### UINT64 *= 'UINT64'*

<a id="mlserver.types.Datatype.INT8"></a>

#### INT8 *= 'INT8'*

<a id="mlserver.types.Datatype.INT16"></a>

#### INT16 *= 'INT16'*

<a id="mlserver.types.Datatype.INT32"></a>

#### INT32 *= 'INT32'*

<a id="mlserver.types.Datatype.INT64"></a>

#### INT64 *= 'INT64'*

<a id="mlserver.types.Datatype.FP16"></a>

#### FP16 *= 'FP16'*

<a id="mlserver.types.Datatype.FP32"></a>

#### FP32 *= 'FP32'*

<a id="mlserver.types.Datatype.FP64"></a>

#### FP64 *= 'FP64'*

<a id="mlserver.types.Datatype.BYTES"></a>

#### BYTES *= 'BYTES'*

<a id="mlserver.types.MetadataTensor"></a>

### *pydantic model* mlserver.types.MetadataTensor

Bases: `BaseModel`

* **Fields:**
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

<a id="mlserver.types.MetadataTensor.datatype"></a>

#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]*

<a id="mlserver.types.MetadataTensor.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.MetadataTensor.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.MetadataTensor.shape"></a>

#### *field* shape *: List[int]* *[Required]*

<a id="mlserver.types.MetadataModelErrorResponse"></a>

### *pydantic model* mlserver.types.MetadataModelErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str)`

<a id="mlserver.types.MetadataModelErrorResponse.error"></a>

#### *field* error *: str* *[Required]*

<a id="mlserver.types.Parameters"></a>

### *pydantic model* mlserver.types.Parameters

Bases: `BaseModel`

* **Fields:**
  - `content_type (str | None)`
  - `headers (Dict[str, Any] | None)`

<a id="mlserver.types.Parameters.content_type"></a>

#### *field* content_type *: str | None* *= None*

<a id="mlserver.types.Parameters.headers"></a>

#### *field* headers *: Dict[str, Any] | None* *= None*

<a id="mlserver.types.TensorData"></a>

### *pydantic model* mlserver.types.TensorData

Bases: `RootModel[Union[List, Any]]`

* **Fields:**
  - `root (List | Any)`

<a id="mlserver.types.TensorData.root"></a>

#### *field* root *: List | Any* *[Required]*

<a id="mlserver.types.RequestOutput"></a>

### *pydantic model* mlserver.types.RequestOutput

Bases: `BaseModel`

* **Fields:**
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

<a id="mlserver.types.RequestOutput.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.RequestOutput.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.ResponseOutput"></a>

### *pydantic model* mlserver.types.ResponseOutput

Bases: `BaseModel`

* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

<a id="mlserver.types.ResponseOutput.data"></a>

#### *field* data *: [TensorData](#mlserver.types.TensorData)* *[Required]*

<a id="mlserver.types.ResponseOutput.datatype"></a>

#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]*

<a id="mlserver.types.ResponseOutput.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.ResponseOutput.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.ResponseOutput.shape"></a>

#### *field* shape *: List[int]* *[Required]*

<a id="mlserver.types.InferenceResponse"></a>

### *pydantic model* mlserver.types.InferenceResponse

Bases: `BaseModel`

* **Fields:**
  - `id (str | None)`
  - `model_name (str)`
  - `model_version (str | None)`
  - `outputs (List[mlserver.types.dataplane.ResponseOutput])`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

<a id="mlserver.types.InferenceResponse.id"></a>

#### *field* id *: str | None* *= None*

<a id="mlserver.types.InferenceResponse.model_name"></a>

#### *field* model_name *: str* *[Required]*

<a id="mlserver.types.InferenceResponse.model_version"></a>

#### *field* model_version *: str | None* *= None*

<a id="mlserver.types.InferenceResponse.outputs"></a>

#### *field* outputs *: List[[ResponseOutput](#mlserver.types.ResponseOutput)]* *[Required]*

<a id="mlserver.types.InferenceResponse.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.InferenceErrorResponse"></a>

### *pydantic model* mlserver.types.InferenceErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`

<a id="mlserver.types.InferenceErrorResponse.error"></a>

#### *field* error *: str | None* *= None*

<a id="mlserver.types.MetadataModelResponse"></a>

### *pydantic model* mlserver.types.MetadataModelResponse

Bases: `BaseModel`

* **Fields:**
  - `inputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `name (str)`
  - `outputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `platform (str)`
  - `versions (List[str] | None)`

<a id="mlserver.types.MetadataModelResponse.inputs"></a>

#### *field* inputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None*

<a id="mlserver.types.MetadataModelResponse.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.MetadataModelResponse.outputs"></a>

#### *field* outputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None*

<a id="mlserver.types.MetadataModelResponse.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.MetadataModelResponse.platform"></a>

#### *field* platform *: str* *[Required]*

<a id="mlserver.types.MetadataModelResponse.versions"></a>

#### *field* versions *: List[str] | None* *= None*

<a id="mlserver.types.RequestInput"></a>

### *pydantic model* mlserver.types.RequestInput

Bases: `BaseModel`

* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

<a id="mlserver.types.RequestInput.data"></a>

#### *field* data *: [TensorData](#mlserver.types.TensorData)* *[Required]*

<a id="mlserver.types.RequestInput.datatype"></a>

#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]*

<a id="mlserver.types.RequestInput.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.RequestInput.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.RequestInput.shape"></a>

#### *field* shape *: List[int]* *[Required]*

<a id="mlserver.types.InferenceRequest"></a>

### *pydantic model* mlserver.types.InferenceRequest

Bases: `BaseModel`

* **Fields:**
  - `id (str | None)`
  - `inputs (List[mlserver.types.dataplane.RequestInput])`
  - `outputs (List[mlserver.types.dataplane.RequestOutput] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

<a id="mlserver.types.InferenceRequest.id"></a>

#### *field* id *: str | None* *= None*

<a id="mlserver.types.InferenceRequest.inputs"></a>

#### *field* inputs *: List[[RequestInput](#mlserver.types.RequestInput)]* *[Required]*

<a id="mlserver.types.InferenceRequest.outputs"></a>

#### *field* outputs *: List[[RequestOutput](#mlserver.types.RequestOutput)] | None* *= None*

<a id="mlserver.types.InferenceRequest.parameters"></a>

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

<a id="mlserver.types.RepositoryIndexRequest"></a>

### *pydantic model* mlserver.types.RepositoryIndexRequest

Bases: `BaseModel`

* **Fields:**
  - `ready (bool | None)`

<a id="mlserver.types.RepositoryIndexRequest.ready"></a>

#### *field* ready *: bool | None* *= None*

<a id="mlserver.types.RepositoryIndexResponseItem"></a>

### *pydantic model* mlserver.types.RepositoryIndexResponseItem

Bases: `BaseModel`

* **Fields:**
  - `name (str)`
  - `reason (str)`
  - `state (mlserver.types.model_repository.State)`
  - `version (str | None)`

<a id="mlserver.types.RepositoryIndexResponseItem.name"></a>

#### *field* name *: str* *[Required]*

<a id="mlserver.types.RepositoryIndexResponseItem.reason"></a>

#### *field* reason *: str* *[Required]*

<a id="mlserver.types.RepositoryIndexResponseItem.state"></a>

#### *field* state *: [State](#mlserver.types.State)* *[Required]*

<a id="mlserver.types.RepositoryIndexResponseItem.version"></a>

#### *field* version *: str | None* *= None*

<a id="mlserver.types.State"></a>

### *class* mlserver.types.State

Bases: `Enum`

<a id="mlserver.types.State.UNKNOWN"></a>

#### UNKNOWN *= 'UNKNOWN'*

<a id="mlserver.types.State.READY"></a>

#### READY *= 'READY'*

<a id="mlserver.types.State.UNAVAILABLE"></a>

#### UNAVAILABLE *= 'UNAVAILABLE'*

<a id="mlserver.types.State.LOADING"></a>

#### LOADING *= 'LOADING'*

<a id="mlserver.types.State.UNLOADING"></a>

#### UNLOADING *= 'UNLOADING'*

<a id="mlserver.types.RepositoryIndexResponse"></a>

### *pydantic model* mlserver.types.RepositoryIndexResponse

Bases: `RootModel[List[RepositoryIndexResponseItem]]`

* **Fields:**
  - `root (List[mlserver.types.model_repository.RepositoryIndexResponseItem])`

<a id="mlserver.types.RepositoryIndexResponse.root"></a>

#### *field* root *: List[[RepositoryIndexResponseItem](#mlserver.types.RepositoryIndexResponseItem)]* *[Required]*

<a id="mlserver.types.RepositoryLoadErrorResponse"></a>

### *pydantic model* mlserver.types.RepositoryLoadErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`

<a id="mlserver.types.RepositoryLoadErrorResponse.error"></a>

#### *field* error *: str | None* *= None*

<a id="mlserver.types.RepositoryUnloadErrorResponse"></a>

### *pydantic model* mlserver.types.RepositoryUnloadErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`

<a id="mlserver.types.RepositoryUnloadErrorResponse.error"></a>

#### *field* error *: str | None* *= None*
