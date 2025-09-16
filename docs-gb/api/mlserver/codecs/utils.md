# Module `mlserver.codecs.utils`


## Class `SingleInputRequestCodec`


**Description:**
The SingleInputRequestCodec can be used as a "meta-implementation" for other
codecs. Its goal to decode the whole request simply as the first decoded
element.

## Function `decode_inference_request`


**Signature:** `decode_inference_request(inference_request: mlserver.types.dataplane.InferenceRequest, model_settings: Optional[mlserver.settings.ModelSettings] = None, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]`


**Description:**
*No docstring available.*

## Function `decode_request_input`


**Signature:** `decode_request_input(request_input: mlserver.types.dataplane.RequestInput, metadata_inputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[Any]`


**Description:**
*No docstring available.*

## Function `encode_inference_response`


**Signature:** `encode_inference_response(payload: Any, model_settings: mlserver.settings.ModelSettings) -> Optional[mlserver.types.dataplane.InferenceResponse]`


**Description:**
*No docstring available.*

## Function `encode_response_output`


**Signature:** `encode_response_output(payload: Any, request_output: mlserver.types.dataplane.RequestOutput, metadata_outputs: Dict[str, mlserver.types.dataplane.MetadataTensor] = {}) -> Optional[mlserver.types.dataplane.ResponseOutput]`


**Description:**
*No docstring available.*

## Function `get_decoded`


**Signature:** `get_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any`


**Description:**
*No docstring available.*

## Function `get_decoded_or_raw`


**Signature:** `get_decoded_or_raw(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> Any`


**Description:**
*No docstring available.*

## Function `has_decoded`


**Signature:** `has_decoded(parametrised_obj: Union[mlserver.types.dataplane.InferenceRequest, mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.RequestOutput, mlserver.types.dataplane.ResponseOutput, mlserver.types.dataplane.InferenceResponse]) -> bool`


**Description:**
*No docstring available.*

## Function `inject_batch_dimension`


**Signature:** `inject_batch_dimension(shape: List[int]) -> List[int]`


**Description:**
Utility method to ensure that 1-dimensional shapes
assume that `[N] == [N, D]`.
