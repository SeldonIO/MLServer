# Module `mlserver.cache.cache`


## Class `ResponseCache`


**Description:**
*No docstring available.*

### Method `insert`


**Signature:** `insert(self, key: str, value: str)`


**Description:**
Method responsible for inserting value to cache.
**This method should be overriden to implement your custom cache logic.**

### Method `lookup`


**Signature:** `lookup(self, key: str) -> str`


**Description:**
Method responsible for returning key value in the cache.
**This method should be overriden to implement your custom cache logic.**

### Method `size`


**Signature:** `size(self) -> int`


**Description:**
Method responsible for returning the size of the cache.
**This method should be overriden to implement your custom cache logic.**
