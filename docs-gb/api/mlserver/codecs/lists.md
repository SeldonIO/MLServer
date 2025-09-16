# Module `mlserver.codecs.lists`


## Function `as_list`


**Signature:** `as_list(payload: Union[bytes, str, List[Union[bytes, str]]]) -> Iterator[Union[bytes, str]]`


**Description:**
Return a payload as an iterator. Single elements will be
treated as a list of 1 item. All elements are assumed to be
string-like.

## Function `is_list_of`


**Signature:** `is_list_of(payload: Any, instance_type: Type)`


**Description:**
*No docstring available.*
