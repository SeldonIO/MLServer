# Types

### *pydantic model* mlserver.types.MetadataServerResponse

Bases: `BaseModel`

* **Fields:**
  - `extensions (List[str])`
  - `name (str)`
  - `version (str)`

#### *field* extensions *: List[str]* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* version *: str* *[Required]*

### *pydantic model* mlserver.types.MetadataServerErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str)`

#### *field* error *: str* *[Required]*

### *class* mlserver.types.Datatype

Bases: `Enum`

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

### *pydantic model* mlserver.types.MetadataTensor

Bases: `BaseModel`

* **Fields:**
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### *field* shape *: List[int]* *[Required]*

### *pydantic model* mlserver.types.MetadataModelErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str)`

#### *field* error *: str* *[Required]*

### *pydantic model* mlserver.types.Parameters

Bases: `BaseModel`

* **Fields:**
  - `content_type (str | None)`
  - `headers (Dict[str, Any] | None)`

#### *field* content_type *: str | None* *= None*

#### *field* headers *: Dict[str, Any] | None* *= None*

### *pydantic model* mlserver.types.TensorData

Bases: `RootModel[Union[List, Any]]`

* **Fields:**
  - `root (List | Any)`

#### *field* root *: List | Any* *[Required]*

### *pydantic model* mlserver.types.RequestOutput

Bases: `BaseModel`

* **Fields:**
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* name *: str* *[Required]*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

### *pydantic model* mlserver.types.ResponseOutput

Bases: `BaseModel`

* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

#### *field* data *: [TensorData](#mlserver.types.TensorData)* *[Required]*

#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### *field* shape *: List[int]* *[Required]*

### *pydantic model* mlserver.types.InferenceResponse

Bases: `BaseModel`

* **Fields:**
  - `id (str | None)`
  - `model_name (str)`
  - `model_version (str | None)`
  - `outputs (List[mlserver.types.dataplane.ResponseOutput])`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* id *: str | None* *= None*

#### *field* model_name *: str* *[Required]*

#### *field* model_version *: str | None* *= None*

#### *field* outputs *: List[[ResponseOutput](#mlserver.types.ResponseOutput)]* *[Required]*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

### *pydantic model* mlserver.types.InferenceErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

### *pydantic model* mlserver.types.MetadataModelResponse

Bases: `BaseModel`

* **Fields:**
  - `inputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `name (str)`
  - `outputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `platform (str)`
  - `versions (List[str] | None)`

#### *field* inputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None*

#### *field* name *: str* *[Required]*

#### *field* outputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### *field* platform *: str* *[Required]*

#### *field* versions *: List[str] | None* *= None*

### *pydantic model* mlserver.types.RequestInput

Bases: `BaseModel`

* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`

#### *field* data *: [TensorData](#mlserver.types.TensorData)* *[Required]*

#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### *field* shape *: List[int]* *[Required]*

### *pydantic model* mlserver.types.InferenceRequest

Bases: `BaseModel`

* **Fields:**
  - `id (str | None)`
  - `inputs (List[mlserver.types.dataplane.RequestInput])`
  - `outputs (List[mlserver.types.dataplane.RequestOutput] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* id *: str | None* *= None*

#### *field* inputs *: List[[RequestInput](#mlserver.types.RequestInput)]* *[Required]*

#### *field* outputs *: List[[RequestOutput](#mlserver.types.RequestOutput)] | None* *= None*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

### *pydantic model* mlserver.types.RepositoryIndexRequest

Bases: `BaseModel`

* **Fields:**
  - `ready (bool | None)`

#### *field* ready *: bool | None* *= None*

### *pydantic model* mlserver.types.RepositoryIndexResponseItem

Bases: `BaseModel`

* **Fields:**
  - `name (str)`
  - `reason (str)`
  - `state (mlserver.types.model_repository.State)`
  - `version (str | None)`

#### *field* name *: str* *[Required]*

#### *field* reason *: str* *[Required]*

#### *field* state *: [State](#mlserver.types.State)* *[Required]*

#### *field* version *: str | None* *= None*

### *class* mlserver.types.State

Bases: `Enum`

#### UNKNOWN *= 'UNKNOWN'*

#### READY *= 'READY'*

#### UNAVAILABLE *= 'UNAVAILABLE'*

#### LOADING *= 'LOADING'*

#### UNLOADING *= 'UNLOADING'*

### *pydantic model* mlserver.types.RepositoryIndexResponse

Bases: `RootModel[List[RepositoryIndexResponseItem]]`

* **Fields:**
  - `root (List[mlserver.types.model_repository.RepositoryIndexResponseItem])`

#### *field* root *: List[[RepositoryIndexResponseItem](#mlserver.types.RepositoryIndexResponseItem)]* *[Required]*

### *pydantic model* mlserver.types.RepositoryLoadErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

### *pydantic model* mlserver.types.RepositoryUnloadErrorResponse

Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*
