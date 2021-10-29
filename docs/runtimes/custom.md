# Creating custom inference runtimes

There may be cases where the [inference runtimes](../index) offered
out-of-the-box by MLServer may not be enough, or where you may need extra
custom functionality which is not included in MLServer (e.g. custom codecs).
To cover these cases, MLServer lets you create custom runtimes very easily.

This page covers some of the bigger points that need to be taken into account
when extending MLServer.
You can also see this [end-to-end example](../example/custom/README) which
walks through the process of writing a custom runtime.

## Writing a custom runtime

MLServer is designed as an easy-to-extend framework, encouraging users to write
their own custom runtimes easily.
The starting point for this is the `mlserver.MLModel` abstract class, whose
main methods are:

- `load(self) -> bool`:
  Responsible for loading any artifacts related to a model (e.g. model
  weights, pickle files, etc.).
- `predict(self, payload: InferenceRequest) -> InferenceResponse`:
  Responsible for using a model to perform inference on an incoming data point.

Therefore, the _"one-line version"_ of how to write a custom runtime is to
write a custom class, extending from `mlserver.MLModel`, and then overriding
those methods with your custom logic.

```python
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse

class MyCustomRuntime(MLModel):

  def load(self) -> bool:
    # Replace for custom logic to load a model artifact
    self._model = load_my_custom_model()
    self.ready = True
    return self.ready

  def predict(self, payload: InferenceRequest) -> InferenceResponse:
    # Replace for custom logic to run inference
    return self._model.predict(payload)
```

## Building a custom MLServer image

MLServer offers built-in utilities to help you build a custom MLServer image.
This image can contain any custom code (including custom inference runtimes),
as well as any custom environment, provided either through a [Conda environment
file](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
or a `requirements.txt` file.
