# Codecs

## Methods

# Module `mlserver.codecs`

## Functions

### `decode_args`
```python
decode_args(predict: Callable) -> Callable[[ForwardRef('MLModel'), mlserver.types.dataplane.InferenceRequest], Coroutine[Any, Any, mlserver.types.dataplane.InferenceResponse]]
```
-

### `decode_inference_request`
```python
decode_inference_request(inference_request: mlserver.types.dataplane.InferenceRequest, model_settings: Optional[mlserver.settings.ModelSettings] = None, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```
-

### `decode_request_input`
```python
decode_request_input(request_input: mlserver.types.dataplane.RequestInput, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]
```
-

### `encode_inference_response`
```python
encode_inference_response(payload: Any, model_settings: mlserver.settings.ModelSettings) -> Optional[mlserver.types.dataplane.InferenceResponse]
```
-

### `encode_response_output`
```python
encode_response_output(payload: Any, request_output: mlserver.types.dataplane.RequestOutput, metadata_outputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[mlserver.types.dataplane.ResponseOutput]
```
-

### `get_decoded`
```python
get_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```
-

### `get_decoded_or_raw`
```python
get_decoded_or_raw(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any
```
-

### `has_decoded`
```python
has_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> bool
```
-

### `register_input_codec`
```python
register_input_codec(CodecKlass: Union[Type[ForwardRef('InputCodec')], ForwardRef('InputCodec')])
```
-

### `register_request_codec`
```python
register_request_codec(CodecKlass: Union[Type[ForwardRef('RequestCodec')], ForwardRef('RequestCodec')])
```
-


