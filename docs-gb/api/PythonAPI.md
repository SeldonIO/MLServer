# Python API

MLServer exposes a Python framework to build custom inference runtimes, define request/response types, plug codecs for payload conversion, and emit metrics. This page provides a high-level overview and links to the API docs.

- [MLModel](./MLModel.md)
  - Base class to implement custom inference runtimes.
  - Core lifecycle: `load()`, `predict()`, `unload()`.
  - Helpers for encoding/decoding requests and responses.
  - Access to model metadata and settings.
  - Extend this class to implement your own model logic.
- [Types](./Types.md)
  - Data structures and enums for the V2 inference protocol.
  - Includes Pydantic models like `InferenceRequest`, `InferenceResponse`, `RequestInput`, `ResponseOutput`.
  - See model fields (type and default) and JSON Schemas in the docs.
- [Codecs](./Codecs.md)
  - Encode/decode payloads between Open Inference Protocol types and Python types.
  - Base classes: `InputCodec` (inputs/outputs) and `RequestCodec` (requests/responses).
  - Built-ins include codecs such as `NumpyCodec`, `Base64Codec`, `StringCodec`, etc.
- [Metrics](./Metrics.md)
  - Emit and configure metrics within MLServer.
  - Use `log()` to record custom metrics; see server lifecycle hooks and utilities.

{% hint style="tip" %}
When creating a custom runtime, start by subclassing `MLModel`, use the structures from [Types](./Types.md) for requests/responses, pick or implement the appropriate [Codecs](./Codecs.md), and optionally emit [Metrics](./Metrics.md) from your model code.
{% endhint %}





