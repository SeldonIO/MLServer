# Types

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
* **Fields:**
  - `extensions (List[str])`
  - `name (str)`
  - `version (str)`

#### *field* extensions *: List[str]* *[Required]*

#### *field* name *: str* *[Required]*

#### *field* version *: str* *[Required]*

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
* **Fields:**
  - `error (str)`

#### *field* error *: str* *[Required]*

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
* **Fields:**
  - `content_type (str | None)`
  - `headers (Dict[str, Any] | None)`

#### *field* content_type *: str | None* *= None*

#### *field* headers *: Dict[str, Any] | None* *= None*

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
* **Fields:**
  - `name (str)`
  - `parameters (mlserver.types.dataplane.Parameters | None)`

#### *field* name *: str* *[Required]*

#### *field* parameters *: [Parameters](#mlserver.types.Parameters) | None* *= None*

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
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

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
* **Fields:**
  - `ready (bool | None)`

#### *field* ready *: bool | None* *= None*

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

#### *field* root *: List[[RepositoryIndexResponseItem](#mlserver.types.RepositoryIndexResponseItem)]* *[Required]*

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
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*

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
* **Fields:**
  - `error (str | None)`

#### *field* error *: str | None* *= None*
