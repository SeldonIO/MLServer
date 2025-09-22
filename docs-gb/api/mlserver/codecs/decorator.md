# Module `mlserver.codecs.decorator`


## Class `SignatureCodec`


**Description:**
Internal codec that knows how to map type hints to codecs.

### Method `decode_request`


**Signature:** `decode_request(self, request: mlserver.types.dataplane.InferenceRequest) -> Dict[str, Any]`


**Description:**
Decode an inference request into a high-level Python object.

### Method `encode_response`


**Signature:** `encode_response(self, model_name: str, payload: Any, model_version: Optional[str] = None) -> mlserver.types.dataplane.InferenceResponse`


**Description:**
Encode the given payload into an inference response.

## Function `decode_args`


**Signature:** `decode_args(predict: Callable) -> Callable[[ForwardRef('MLModel'), mlserver.types.dataplane.InferenceRequest], Coroutine[Any, Any, mlserver.types.dataplane.InferenceResponse]]`


**Description:**
*No docstring available.*
