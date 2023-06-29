# MLModel

The `MLModel` class is the base class for all [custom inference
runtimes](../../user-guide/custom).
It exposes the main interface that MLServer will use to interact with ML
models.

The bulk of its public interface are the {func}`load()
<mlserver.MLModel.load>`, {func}`unload() <mlserver.MLModel.unload>` and
{func}`predict() <mlserver.MLModel.predict>` methods.
However, it also contains helpers with encoding / decoding of requests and
responses, as well as properties to access the most common bits of the model's
metadata.

When writing [custom runtimes](../../user-guide/custom), **this class should be
extended to implement your own load and predict logic**.

```{eval-rst}
.. autoclass:: mlserver.MLModel
   :members:
   :member-order: bysource
```
