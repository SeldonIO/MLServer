# Module `mlserver.batching.hooks`


## Class `InvalidBatchingMethod`


**Description:**
Common base class for all non-exit exceptions.

## Function `adaptive_batching`


**Signature:** `adaptive_batching(f: Callable[[mlserver.types.dataplane.InferenceRequest], Awaitable[mlserver.types.dataplane.InferenceResponse]])`


**Description:**
Decorator for the `predict()` method which will ensure it uses the
underlying adaptive batcher instance.

## Function `load_batching`


**Signature:** `load_batching(model: mlserver.model.MLModel) -> mlserver.model.MLModel`


**Description:**
*No docstring available.*

## Function `not_implemented_warning`


**Signature:** `not_implemented_warning(f: Callable[[AsyncIterator[mlserver.types.dataplane.InferenceRequest]], AsyncIterator[mlserver.types.dataplane.InferenceResponse]])`


**Description:**
Decorator to lets users know that adaptive batching is not required on
method `f`.
