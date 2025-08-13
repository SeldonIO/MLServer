# MLModel

The `MLModel` class is the base class for all custom inference runtimes.
It exposes the main interface that MLServer will use to interact with ML
models.

The bulk of its public interface are the `load()`, `unload()` and
`predict()` methods. However, it also contains helpers with encoding / decoding of requests and
responses, as well as properties to access the most common bits of the model’s
metadata.

When writing custom runtimes, **this class should be
extended to implement your own load and predict logic**.

# [`mlserver.model`](reference.md#module-mlserver.model)

## Module Contents
