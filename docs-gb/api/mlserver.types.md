# mlserver.types

### *class* mlserver.types.MetadataServerResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### version *: str*

#### extensions *: List[str]*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.MetadataServerErrorResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### error *: str*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.Datatype(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

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

### *class* mlserver.types.MetadataTensor(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### datatype *: [Datatype](#mlserver.types.Datatype)*

#### shape *: List[int]*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.MetadataModelErrorResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### error *: str*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.Parameters(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### content_type *: str | None* *= None*

#### headers *: Dict[str, Any] | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.TensorData(\*args: Any, \*\*kwargs: Any)

Bases: `Any]`

#### root *: List | Any* *= Ellipsis*

### *class* mlserver.types.RequestOutput(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.ResponseOutput(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### shape *: List[int]*

#### datatype *: [Datatype](#mlserver.types.Datatype)*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### data *: [TensorData](#mlserver.types.TensorData)*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.InferenceResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### model_name *: str*

#### model_version *: str | None* *= None*

#### id *: str | None* *= None*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### outputs *: List[[ResponseOutput](#mlserver.types.ResponseOutput)]*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.InferenceErrorResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### error *: str | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.MetadataModelResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### versions *: List[str] | None* *= None*

#### platform *: str*

#### inputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None*

#### outputs *: List[[MetadataTensor](#mlserver.types.MetadataTensor)] | None* *= None*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.RequestInput(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### shape *: List[int]*

#### datatype *: [Datatype](#mlserver.types.Datatype)*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### data *: [TensorData](#mlserver.types.TensorData)*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.InferenceRequest(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### id *: str | None* *= None*

#### parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

#### inputs *: List[[RequestInput](#mlserver.types.RequestInput)]*

#### outputs *: List[[RequestOutput](#mlserver.types.RequestOutput)] | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.RepositoryIndexRequest(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### ready *: bool | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.RepositoryIndexResponseItem(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### name *: str*

#### version *: str | None* *= None*

#### state *: [State](#mlserver.types.State)*

#### reason *: str*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.State(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `Enum`

#### UNKNOWN *= 'UNKNOWN'*

#### READY *= 'READY'*

#### UNAVAILABLE *= 'UNAVAILABLE'*

#### LOADING *= 'LOADING'*

#### UNLOADING *= 'UNLOADING'*

### *class* mlserver.types.RepositoryIndexResponse(\*args: Any, \*\*kwargs: Any)

Bases: `RepositoryIndexResponseItem]`

#### root *: List[[RepositoryIndexResponseItem](#mlserver.types.RepositoryIndexResponseItem)]* *= Ellipsis*

### *class* mlserver.types.RepositoryLoadErrorResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### error *: str | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)

### *class* mlserver.types.RepositoryUnloadErrorResponse(\*args: Any, \*\*kwargs: Any)

Bases: `BaseModel`

#### error *: str | None* *= None*

#### model_dump(exclude_unset=True, exclude_none=True, \*\*kwargs)

#### model_dump_json(exclude_unset=True, exclude_none=True, \*\*kwargs)
