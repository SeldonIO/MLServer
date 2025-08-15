<a id="module-mlserver.types"></a>
# Types {#types}### *pydantic model* mlserver.types.MetadataServerResponse {#mlserver.types.MetadataServerResponse}
Bases: `BaseModel`

* **Fields:**
  - `extensions (List[str])`
  - `name (str)`
  - `version (str)`
#### *field* extensions *: List[str]* *[Required]* {#mlserver.types.MetadataServerResponse.extensions}#### *field* name *: str* *[Required]* {#mlserver.types.MetadataServerResponse.name}#### *field* version *: str* *[Required]* {#mlserver.types.MetadataServerResponse.version}### *pydantic model* mlserver.types.MetadataServerErrorResponse {#mlserver.types.MetadataServerErrorResponse}
Bases: `BaseModel`

* **Fields:**
  - `error (str)`
#### *field* error *: str* *[Required]* {#mlserver.types.MetadataServerErrorResponse.error}### *class* mlserver.types.Datatype {#mlserver.types.Datatype}
Bases: `Enum`
#### BOOL *= 'BOOL'* {#mlserver.types.Datatype.BOOL}#### UINT8 *= 'UINT8'* {#mlserver.types.Datatype.UINT8}#### UINT16 *= 'UINT16'* {#mlserver.types.Datatype.UINT16}#### UINT32 *= 'UINT32'* {#mlserver.types.Datatype.UINT32}#### UINT64 *= 'UINT64'* {#mlserver.types.Datatype.UINT64}#### INT8 *= 'INT8'* {#mlserver.types.Datatype.INT8}#### INT16 *= 'INT16'* {#mlserver.types.Datatype.INT16}#### INT32 *= 'INT32'* {#mlserver.types.Datatype.INT32}#### INT64 *= 'INT64'* {#mlserver.types.Datatype.INT64}#### FP16 *= 'FP16'* {#mlserver.types.Datatype.FP16}#### FP32 *= 'FP32'* {#mlserver.types.Datatype.FP32}#### FP64 *= 'FP64'* {#mlserver.types.Datatype.FP64}#### BYTES *= 'BYTES'* {#mlserver.types.Datatype.BYTES}### *pydantic model* mlserver.types.MetadataTensor {#mlserver.types.MetadataTensor}
Bases: `BaseModel`

* **Fields:**
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`
#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]* {#mlserver.types.MetadataTensor.datatype}#### *field* name *: str* *[Required]* {#mlserver.types.MetadataTensor.name}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.MetadataTensor.parameters}#### *field* shape *: List[int]* *[Required]* {#mlserver.types.MetadataTensor.shape}### *pydantic model* mlserver.types.MetadataModelErrorResponse {#mlserver.types.MetadataModelErrorResponse}
Bases: `BaseModel`

* **Fields:**
  - `error (str)`
#### *field* error *: str* *[Required]* {#mlserver.types.MetadataModelErrorResponse.error}### *pydantic model* mlserver.types.Parameters {#mlserver.types.Parameters}
Bases: `BaseModel`

* **Fields:**
  - `content_type (str | None)`
  - `headers (Dict[str, Any] | None)`
#### *field* content_type *: str | None* *= None* {#mlserver.types.Parameters.content_type}#### *field* headers *: Dict[str, Any] | None* *= None* {#mlserver.types.Parameters.headers}### *pydantic model* mlserver.types.TensorData {#mlserver.types.TensorData}
Bases: `RootModel[Union[List, Any]]`

* **Fields:**
  - `root (List | Any)`
#### *field* root *: List | Any* *[Required]* {#mlserver.types.TensorData.root}### *pydantic model* mlserver.types.RequestOutput {#mlserver.types.RequestOutput}
Bases: `BaseModel`

* **Fields:**
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
#### *field* name *: str* *[Required]* {#mlserver.types.RequestOutput.name}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.RequestOutput.parameters}### *pydantic model* mlserver.types.ResponseOutput {#mlserver.types.ResponseOutput}
Bases: `BaseModel`

* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`
#### *field* data *: [TensorData](#mlserver.types.TensorData)* *[Required]* {#mlserver.types.ResponseOutput.data}#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]* {#mlserver.types.ResponseOutput.datatype}#### *field* name *: str* *[Required]* {#mlserver.types.ResponseOutput.name}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.ResponseOutput.parameters}#### *field* shape *: List[int]* *[Required]* {#mlserver.types.ResponseOutput.shape}### *pydantic model* mlserver.types.InferenceResponse {#mlserver.types.InferenceResponse}
Bases: `BaseModel`

* **Fields:**
  - `id (str | None)`
  - `model_name (str)`
  - `model_version (str | None)`
  - `outputs (List[mlserver.types.dataplane.ResponseOutput])`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
#### *field* id *: str | None* *= None* {#mlserver.types.InferenceResponse.id}#### *field* model_name *: str* *[Required]* {#mlserver.types.InferenceResponse.model_name}#### *field* model_version *: str | None* *= None* {#mlserver.types.InferenceResponse.model_version}#### *field* outputs *: List[[ResponseOutput](#mlserver.types.ResponseOutput)]* *[Required]* {#mlserver.types.InferenceResponse.outputs}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.InferenceResponse.parameters}### *pydantic model* mlserver.types.InferenceErrorResponse {#mlserver.types.InferenceErrorResponse}
Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`
#### *field* error *: str | None* *= None* {#mlserver.types.InferenceErrorResponse.error}### *pydantic model* mlserver.types.MetadataModelResponse {#mlserver.types.MetadataModelResponse}
Bases: `BaseModel`

* **Fields:**
  - `inputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `name (str)`
  - `outputs (List[mlserver.types.dataplane.MetadataTensor] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `platform (str)`
  - `versions (List[str] | None)`
#### *field* inputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None* {#mlserver.types.MetadataModelResponse.inputs}#### *field* name *: str* *[Required]* {#mlserver.types.MetadataModelResponse.name}#### *field* outputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None* {#mlserver.types.MetadataModelResponse.outputs}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.MetadataModelResponse.parameters}#### *field* platform *: str* *[Required]* {#mlserver.types.MetadataModelResponse.platform}#### *field* versions *: List[str] | None* *= None* {#mlserver.types.MetadataModelResponse.versions}### *pydantic model* mlserver.types.RequestInput {#mlserver.types.RequestInput}
Bases: `BaseModel`

* **Fields:**
  - `data (mlserver.types.dataplane.TensorData)`
  - `datatype (mlserver.types.dataplane.Datatype)`
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
  - `shape (List[int])`
#### *field* data *: [TensorData](#mlserver.types.TensorData)* *[Required]* {#mlserver.types.RequestInput.data}#### *field* datatype *: [Datatype](#mlserver.types.Datatype)* *[Required]* {#mlserver.types.RequestInput.datatype}#### *field* name *: str* *[Required]* {#mlserver.types.RequestInput.name}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.RequestInput.parameters}#### *field* shape *: List[int]* *[Required]* {#mlserver.types.RequestInput.shape}### *pydantic model* mlserver.types.InferenceRequest {#mlserver.types.InferenceRequest}
Bases: `BaseModel`

* **Fields:**
  - `id (str | None)`
  - `inputs (List[mlserver.types.dataplane.RequestInput])`
  - `outputs (List[mlserver.types.dataplane.RequestOutput] | None)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`
#### *field* id *: str | None* *= None* {#mlserver.types.InferenceRequest.id}#### *field* inputs *: List[[RequestInput](#mlserver.types.RequestInput)]* *[Required]* {#mlserver.types.InferenceRequest.inputs}#### *field* outputs *: List[[RequestOutput](#mlserver.types.RequestOutput)] | None* *= None* {#mlserver.types.InferenceRequest.outputs}#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None* {#mlserver.types.InferenceRequest.parameters}### *pydantic model* mlserver.types.RepositoryIndexRequest {#mlserver.types.RepositoryIndexRequest}
Bases: `BaseModel`

* **Fields:**
  - `ready (bool | None)`
#### *field* ready *: bool | None* *= None* {#mlserver.types.RepositoryIndexRequest.ready}### *pydantic model* mlserver.types.RepositoryIndexResponseItem {#mlserver.types.RepositoryIndexResponseItem}
Bases: `BaseModel`

* **Fields:**
  - `name (str)`
  - `reason (str)`
  - `state (mlserver.types.model_repository.State)`
  - `version (str | None)`
#### *field* name *: str* *[Required]* {#mlserver.types.RepositoryIndexResponseItem.name}#### *field* reason *: str* *[Required]* {#mlserver.types.RepositoryIndexResponseItem.reason}#### *field* state *: [State](#mlserver.types.State)* *[Required]* {#mlserver.types.RepositoryIndexResponseItem.state}#### *field* version *: str | None* *= None* {#mlserver.types.RepositoryIndexResponseItem.version}### *class* mlserver.types.State {#mlserver.types.State}
Bases: `Enum`
#### UNKNOWN *= 'UNKNOWN'* {#mlserver.types.State.UNKNOWN}#### READY *= 'READY'* {#mlserver.types.State.READY}#### UNAVAILABLE *= 'UNAVAILABLE'* {#mlserver.types.State.UNAVAILABLE}#### LOADING *= 'LOADING'* {#mlserver.types.State.LOADING}#### UNLOADING *= 'UNLOADING'* {#mlserver.types.State.UNLOADING}### *pydantic model* mlserver.types.RepositoryIndexResponse {#mlserver.types.RepositoryIndexResponse}
Bases: `RootModel[List[RepositoryIndexResponseItem]]`

* **Fields:**
  - `root (List[mlserver.types.model_repository.RepositoryIndexResponseItem])`
#### *field* root *: List[[RepositoryIndexResponseItem](#mlserver.types.RepositoryIndexResponseItem)]* *[Required]* {#mlserver.types.RepositoryIndexResponse.root}### *pydantic model* mlserver.types.RepositoryLoadErrorResponse {#mlserver.types.RepositoryLoadErrorResponse}
Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`
#### *field* error *: str | None* *= None* {#mlserver.types.RepositoryLoadErrorResponse.error}### *pydantic model* mlserver.types.RepositoryUnloadErrorResponse {#mlserver.types.RepositoryUnloadErrorResponse}
Bases: `BaseModel`

* **Fields:**
  - `error (str | None)`
#### *field* error *: str | None* *= None* {#mlserver.types.RepositoryUnloadErrorResponse.error}