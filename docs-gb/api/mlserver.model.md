# mlserver.model

### *class* MLModel(settings: ModelSettings)

Abstract inference runtime which exposes the main interface to interact
with ML models.

#### *async* load()

Method responsible for loading the model from a model artefact.
This method will be called on each of the parallel workers (when
parallel inference) is
enabled).
Its return value will represent the model’s readiness status.
A return value of `True` will mean the model is ready.

**This method can be overriden to implement your custom load
logic.**

#### *async* predict(payload: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest))

Method responsible for running inference on the model.

**This method can be overriden to implement your custom inference
logic.**

#### *async* predict_stream(payloads: AsyncIterator[[InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest)])

Method responsible for running generation on the model, streaming a set
of responses back to the client.

**This method can be overriden to implement your custom inference
logic.**

#### *async* unload()

Method responsible for unloading the model, freeing any resources (e.g.
CPU memory, GPU memory, etc.).
This method will be called on each of the parallel workers (when
parallel inference) is
enabled).
A return value of `True` will mean the model is now unloaded.

**This method can be overriden to implement your custom unload
logic.**

#### *property* name *: str*

Model name, from the model settings.

#### *property* version *: str | None*

Model version, from the model settings.

#### *property* settings *: ModelSettings*

Model settings.

#### *property* inputs *: List[[MetadataTensor](mlserver.types.md#mlserver.types.MetadataTensor)] | None*

Expected model inputs, from the model settings.

Note that this property can also be modified at model’s load time to
inject any inputs metadata.

#### *property* outputs *: List[[MetadataTensor](mlserver.types.md#mlserver.types.MetadataTensor)] | None*

Expected model outputs, from the model settings.

Note that this property can also be modified at model’s load time to
inject any outputs metadata.

#### decode(request_input: [RequestInput](mlserver.types.md#mlserver.types.RequestInput), default_codec: Type[[InputCodec](mlserver.codecs.md#mlserver.codecs.InputCodec)] | [InputCodec](mlserver.codecs.md#mlserver.codecs.InputCodec) | None = None)

Helper to decode a **request input** into its corresponding high-level
Python object.
This method will find the most appropiate input codec based on the model’s metadata and the
input’s content type.
Otherwise, it will fall back to the codec specified in the
`default_codec` kwarg.

#### decode_request(inference_request: [InferenceRequest](mlserver.types.md#mlserver.types.InferenceRequest), default_codec: Type[[RequestCodec](mlserver.codecs.md#mlserver.codecs.RequestCodec)] | [RequestCodec](mlserver.codecs.md#mlserver.codecs.RequestCodec) | None = None)

Helper to decode an **inference request** into its corresponding
high-level Python object.
This method will find the most appropiate request codec based on the model’s metadata and the
requests’s content type.
Otherwise, it will fall back to the codec specified in the
`default_codec` kwarg.

#### encode_response(payload: Any, default_codec: Type[[RequestCodec](mlserver.codecs.md#mlserver.codecs.RequestCodec)] | [RequestCodec](mlserver.codecs.md#mlserver.codecs.RequestCodec) | None = None)

Helper to encode a high-level Python object into its corresponding
**inference response**.
This method will find the most appropiate request codec based on the payload’s type.
Otherwise, it will fall back to the codec specified in the
`default_codec` kwarg.

#### encode(payload: Any, request_output: [RequestOutput](mlserver.types.md#mlserver.types.RequestOutput), default_codec: Type[[InputCodec](mlserver.codecs.md#mlserver.codecs.InputCodec)] | [InputCodec](mlserver.codecs.md#mlserver.codecs.InputCodec) | None = None)

Helper to encode a high-level Python object into its corresponding
**response output**.
This method will find the most appropiate input codec based on the model’s metadata, request
output’s content type or payload’s type.
Otherwise, it will fall back to the codec specified in the
`default_codec` kwarg.
