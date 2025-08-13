# Types

The types module contains the core data structures and types used throughout
the MLServer framework. These types define the structure of requests, responses,
and metadata that MLServer uses internally.

```{autodoc2-object} mlserver.types
:renderer: myst
```

## Core Data Structures

The main types include:

- **InferenceRequest**: Represents an incoming inference request
- **InferenceResponse**: Represents an outgoing inference response  
- **RequestInput**: Individual input data within a request
- **ResponseOutput**: Individual output data within a response
- **MetadataTensor**: Metadata describing input/output tensors
- **Parameters**: Additional parameters for requests/responses

## Type Safety

All types are designed to work with Python's type system and provide
proper validation and serialization capabilities. 