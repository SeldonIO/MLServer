# mlserver.types.InferenceRequest

### *pydantic model* mlserver.types.InferenceRequest

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
