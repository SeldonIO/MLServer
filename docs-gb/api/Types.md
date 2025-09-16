# Types

## Datatype

An enumeration.

## InferenceErrorResponse

<details><summary>JSON Schema</summary>


```json

{
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
  },
  "title": "InferenceErrorResponse",
  "type": "object"
}

```


</details>

## InferenceRequest

<details><summary>JSON Schema</summary>


```json

{
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
  "required": [
    "inputs"
  ],
  "title": "InferenceRequest",
  "type": "object"
}

```


</details>

## InferenceResponse

<details><summary>JSON Schema</summary>


```json

{
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
  "required": [
    "model_name",
    "outputs"
  ],
  "title": "InferenceResponse",
  "type": "object"
}

```


</details>

## MetadataModelErrorResponse

<details><summary>JSON Schema</summary>


```json

{
  "properties": {
    "error": {
      "title": "Error",
      "type": "string"
    }
  },
  "required": [
    "error"
  ],
  "title": "MetadataModelErrorResponse",
  "type": "object"
}

```


</details>

## MetadataModelResponse

<details><summary>JSON Schema</summary>


```json

{
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
  "required": [
    "name",
    "platform"
  ],
  "title": "MetadataModelResponse",
  "type": "object"
}

```


</details>

## MetadataServerErrorResponse

<details><summary>JSON Schema</summary>


```json

{
  "properties": {
    "error": {
      "title": "Error",
      "type": "string"
    }
  },
  "required": [
    "error"
  ],
  "title": "MetadataServerErrorResponse",
  "type": "object"
}

```


</details>

## MetadataServerResponse

<details><summary>JSON Schema</summary>


```json

{
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
  ],
  "title": "MetadataServerResponse",
  "type": "object"
}

```


</details>

## MetadataTensor

<details><summary>JSON Schema</summary>


```json

{
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
}

```


</details>

## Parameters

<details><summary>JSON Schema</summary>


```json

{
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

```


</details>

## RepositoryIndexRequest

<details><summary>JSON Schema</summary>


```json

{
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
  },
  "title": "RepositoryIndexRequest",
  "type": "object"
}

```


</details>

## RepositoryIndexResponse

<details><summary>JSON Schema</summary>


```json

{
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
  },
  "title": "RepositoryIndexResponse",
  "type": "array"
}

```


</details>

## RepositoryIndexResponseItem

<details><summary>JSON Schema</summary>


```json

{
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
}

```


</details>

## RepositoryLoadErrorResponse

<details><summary>JSON Schema</summary>


```json

{
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
  },
  "title": "RepositoryLoadErrorResponse",
  "type": "object"
}

```


</details>

## RepositoryUnloadErrorResponse

<details><summary>JSON Schema</summary>


```json

{
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
  },
  "title": "RepositoryUnloadErrorResponse",
  "type": "object"
}

```


</details>

## RequestInput

<details><summary>JSON Schema</summary>


```json

{
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
}

```


</details>

## RequestOutput

<details><summary>JSON Schema</summary>


```json

{
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
}

```


</details>

## ResponseOutput

<details><summary>JSON Schema</summary>


```json

{
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
}

```


</details>

## State

An enumeration.

## TensorData

<details><summary>JSON Schema</summary>


```json

{
  "anyOf": [
    {
      "items": {},
      "type": "array"
    },
    {}
  ],
  "title": "TensorData"
}

```


</details>

