# Module `mlserver.codecs.numpy`


## Class `NumpyCodec`


**Description:**
Decodes an request input (response output) as a NumPy array.

## Class `NumpyRequestCodec`


**Description:**
Decodes the first input (output) of request (response) as a NumPy array.
This codec can be useful for cases where the whole payload is a single
NumPy tensor.

## Function `convert_nan`


**Signature:** `convert_nan(val)`


**Description:**
*No docstring available.*

## Function `to_datatype`


**Signature:** `to_datatype(dtype: numpy.dtype) -> mlserver.types.dataplane.Datatype`


**Description:**
*No docstring available.*

## Function `to_dtype`


**Signature:** `to_dtype(input_or_output: Union[mlserver.types.dataplane.RequestInput, mlserver.types.dataplane.ResponseOutput]) -> 'np.dtype'`


**Description:**
*No docstring available.*
