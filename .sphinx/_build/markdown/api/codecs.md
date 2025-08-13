# Codecs

Codecs in MLServer handle the encoding and decoding of requests and responses
between different content types. They provide a flexible way to handle various
data formats and serialization methods.

The codecs module provides:

- **Input Codecs**: For decoding incoming requests
- **Output Codecs**: For encoding outgoing responses
- **Request Codecs**: For handling complete request/response cycles
- **Utility Functions**: For working with encoded/decoded data

## Codec Interface

All codecs implement a common interface that allows MLServer to:

1. **Detect** if a codec can handle a specific content type
2. **Decode** incoming data into Python objects
3. **Encode** Python objects into the appropriate format
4. **Validate** data structures and types

## Built-in Codecs

MLServer comes with several built-in codecs for common formats:

- **JSON**: For JSON-formatted data
- **Numpy**: For NumPy arrays
- **Pandas**: For Pandas DataFrames
- **String**: For plain text data
- **Base64**: For binary data encoded as base64

# [`mlserver.codecs`](reference.md#module-mlserver.codecs)

## Submodules
