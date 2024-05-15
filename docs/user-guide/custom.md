# Custom Inference Runtimes

There may be cases where the [inference runtimes](./index) offered
out-of-the-box by MLServer may not be enough, or where you may need **extra
custom functionality** which is not included in MLServer (e.g. custom codecs).
To cover these cases, MLServer lets you create custom runtimes very easily.

This page covers some of the bigger points that need to be taken into account
when extending MLServer.
You can also see this [end-to-end example](../examples/custom/README) which
walks through the process of writing a custom runtime.

## Writing a custom inference runtime

MLServer is designed as an easy-to-extend framework, encouraging users to write
their own custom runtimes easily.
The starting point for this is the {class}`MLModel <mlserver.MLModel>`
abstract class, whose main methods are:

- {func}`load() <mlserver.MLModel.load>`:
  Responsible for loading any artifacts related to a model (e.g. model
  weights, pickle files, etc.).
- {func}`unload() <mlserver.MLModel.unload>`:
  Responsible for unloading the model, freeing any resources (e.g. GPU memory,
  etc.).
- {func}`predict() <mlserver.MLModel.predict>`:
  Responsible for using a model to perform inference on an incoming data point.

Therefore, the _"one-line version"_ of how to write a custom runtime is to
write a custom class extending from {class}`MLModel <mlserver.MLModel>`,
and then overriding those methods with your custom logic.

```{code-block} python
---
emphasize-lines: 7-8, 12-13
---
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse

class MyCustomRuntime(MLModel):

  async def load(self) -> bool:
    # TODO: Replace for custom logic to load a model artifact
    self._model = load_my_custom_model()
    return True

  async def predict(self, payload: InferenceRequest) -> InferenceResponse:
    # TODO: Replace for custom logic to run inference
    return self._model.predict(payload)
```

### Simplified interface

MLServer exposes an alternative _"simplified" interface_ which can be used to
write custom runtimes.
This interface can be enabled by decorating your `predict()` method with the
`mlserver.codecs.decode_args` decorator.
This will let you specify in the method signature both how you want your
request payload to be decoded and how to encode the response back.

Based on the information provided in the method signature, MLServer will
automatically decode the request payload into the different inputs specified as
keyword arguments.
Under the hood, this is implemented through [MLServer's codecs and content types
system](./content-type.md).

```{note}
MLServer's _"simplified" interface_ aims to cover use cases where encoding /
decoding can be done through one of the codecs built-in into the MLServer
package.
However, there are instances where this may not be enough (e.g. variable number
of inputs, variable content types, etc.).
For these types of cases, please use MLServer's [_"advanced"
interface_](#writing-a-custom-inference-runtime), where you will have full
control over the full encoding / decoding process.
```

As an example of the above, let's assume a model which

- Takes two lists of strings as inputs:
  - `questions`, containing multiple questions to ask our model.
  - `context`, containing multiple contexts for each of the
    questions.
- Returns a Numpy array with some predictions as the output.

Leveraging MLServer's simplified notation, we can represent the above as the
following custom runtime:

```{code-block} python
---
emphasize-lines: 2-3, 12-13
---
from mlserver import MLModel
from mlserver.codecs import decode_args
from typing import List

class MyCustomRuntime(MLModel):

  async def load(self) -> bool:
    # TODO: Replace for custom logic to load a model artifact
    self._model = load_my_custom_model()
    return True

  @decode_args
  async def predict(self, questions: List[str], context: List[str]) -> np.ndarray:
    # TODO: Replace for custom logic to run inference
    return self._model.predict(questions, context)
```

Note that, the method signature of our `predict` method now specifies:

- The input names that we should be looking for in the request
  payload (i.e. `questions` and `context`).
- The expected content type for each of the request inputs (i.e. `List[str]` on
  both cases).
- The expected content type of the response outputs (i.e. `np.ndarray`).

### Read and write headers

```{note}
The `headers` field within the `parameters` section of the request / response
is managed by MLServer.
Therefore, incoming payloads where this field has been explicitly modified will
be overriden.
```

There are occasions where custom logic must be made conditional to extra
information sent by the client outside of the payload.
To allow for these use cases, MLServer will map all incoming HTTP headers (in
the case of REST) or metadata (in the case of gRPC) into the `headers` field of
the `parameters` object within the `InferenceRequest` instance.

```{code-block} python
---
emphasize-lines: 9-11
---
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse

class CustomHeadersRuntime(MLModel):

  ...

  async def predict(self, payload: InferenceRequest) -> InferenceResponse:
    if payload.parameters and payload.parametes.headers:
      # These are all the incoming HTTP headers / gRPC metadata
      print(payload.parameters.headers)
    ...
```

Similarly, to return any HTTP headers (in the case of REST) or metadata (in the
case of gRPC), you can append any values to the `headers` field within the
`parameters` object of the returned `InferenceResponse` instance.

```{code-block} python
---
emphasize-lines: 13
---
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse

class CustomHeadersRuntime(MLModel):

  ...

  async def predict(self, payload: InferenceRequest) -> InferenceResponse:
    ...
    return InferenceResponse(
      # Include any actual outputs from inference
      outputs=[],
      parameters=Parameters(headers={"foo": "bar"})
    )
```

## Loading a custom MLServer runtime

MLServer lets you load custom runtimes dynamically into a running instance of
MLServer.
Once you have your custom runtime ready, all you need to is to move it to your
model folder, next to your `model-settings.json` configuration file.

For example, if we assume a flat model repository where each folder represents
a model, you would end up with a folder structure like the one below:

```bash
.
└── models
    └── sum-model
        ├── model-settings.json
        ├── models.py
```

Note that, from the example above, we are assuming that:

- Your custom runtime code lives in the `models.py` file.
- The `implementation` field of your `model-settings.json` configuration file
  contains the import path of your custom runtime (e.g.
  `models.MyCustomRuntime`).

  ```{code-block} json
  ---
  emphasize-lines: 3
  ---
  {
    "model": "sum-model",
    "implementation": "models.MyCustomRuntime"
  }
  ```

### Loading a custom Python environment

More often that not, your custom runtimes will depend on external 3rd party
dependencies which are not included within the main MLServer package.
In these cases, to load your custom runtime, MLServer will need access to these
dependencies.

It is possible to load this custom set of dependencies by providing them
through an [environment tarball](../examples/conda/README), whose path can be
specified within your `model-settings.json` file.

```{warning}
To load a custom environment, [parallel inference](./parallel-inference)
**must** be enabled.
```

```{warning}
The main MLServer process communicates with workers in custom environments via
[`multiprocessing.Queue`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue)
using pickled objects. Custom environments therefore **must** use the same
version of MLServer and a compatible version of Python with the same [default
pickle protocol](https://docs.python.org/3/library/pickle.html#pickle.DEFAULT_PROTOCOL)
as the main process. Consult the tables below for environment compatibility.
```

| Status | Description  |
| ------ | ------------ |
| 🔴     | Unsupported  |
| 🟢     | Supported    |
| 🔵     | Untested     |

| Worker Python \ Server Python | 3.9 | 3.10 | 3.11 |
| ----------------------------- | --- | ---- | ---- |
| 3.9                           | 🟢  | 🟢   | 🔵   |
| 3.10                          | 🟢  | 🟢   | 🔵   |
| 3.11                          | 🔵  | 🔵   | 🔵   |

If we take the [previous example](#loading-a-custom-mlserver-runtime) above as
a reference, we could extend it to include our custom environment as:

```bash
.
└── models
    └── sum-model
        ├── environment.tar.gz
        ├── model-settings.json
        ├── models.py
```

Note that, in the folder layout above, we are assuming that:

- The `environment.tar.gz` tarball contains a pre-packaged version of your
  custom environment.
- The `environment_tarball` field of your `model-settings.json` configuration file
  points to your pre-packaged custom environment (i.e.
  `./environment.tar.gz`).

  ```{code-block} json
  ---
  emphasize-lines: 5
  ---
  {
    "model": "sum-model",
    "implementation": "models.MyCustomRuntime",
    "parameters": {
      "environment_tarball": "./environment.tar.gz"
    }
  }
  ```

## Building a custom MLServer image

```{note}
The `mlserver build` command expects that a Docker runtime is available and
running in the background.
```

MLServer offers built-in utilities to help you build a custom MLServer image.
This image can contain any custom code (including custom inference runtimes),
as well as any custom environment, provided either through a [Conda environment
file](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
or a `requirements.txt` file.

To leverage these, we can use the `mlserver build` command.
Assuming that we're currently on the folder containing our custom inference
runtime, we should be able to just run:

```bash
mlserver build . -t my-custom-server
```

The output will be a Docker image named `my-custom-server`, ready to be used.

### Custom Environment

The [`mlserver build`](../reference/cli) subcommand will search for any Conda
environment file (i.e. named either as `environment.yaml` or `conda.yaml`) and
/ or any `requirements.txt` present in your root folder.
These can be used to tell MLServer what Python environment is required in the
final Docker image.

```{note}
The environment built by the `mlserver build` will be global to the whole
MLServer image (i.e. every loaded model will, by default, use that custom
environment).
For Multi-Model Serving scenarios, it may be better to use [per-model custom
environments](#loading-a-custom-python-environment) instead - which will allow
you to run multiple custom environments at the same time.
```

### Default Settings

The `mlserver build` subcommand will treat any
[`settings.json`](../reference/settings) or
[`model-settings.json`](../reference/model-settings) files present on your root
folder as the default settings that must be set in your final image.
Therefore, these files can be used to configure things like the default
inference runtime to be used, or to even include **embedded models** that will
always be present within your custom image.

```{note}
Default setting values can still be overriden by external environment variables
or model-specific `model-settings.json`.
```

### Custom Dockerfile

Out-of-the-box, the `mlserver build` subcommand leverages a default
`Dockerfile` which takes into account a number of requirements, like

- Supporting arbitrary user IDs.
- Building your [base custom environment](#custom-environment) on the fly.
- Configure a set of [default setting values](#default-settings).

However, there may be occasions where you need to customise your `Dockerfile`
even further.
This may be the case, for example, when you need to provide extra environment
variables or when you need to customise your Docker build process (e.g. by
using other _"Docker-less"_ tools, like
[Kaniko](https://github.com/GoogleContainerTools/kaniko) or
[Buildah](https://buildah.io/)).

To account for these cases, MLServer also includes a [`mlserver
dockerfile`](../reference/cli) subcommand which will just generate a
`Dockerfile` (and optionally a `.dockerignore` file) exactly like the one used
by the `mlserver build` command.
This `Dockerfile` can then be customised according to your needs.

````{note}
The base `Dockerfile` requires [Docker's
Buildkit](https://docs.docker.com/build/buildkit/) to be enabled.
To ensure BuildKit is used, you can use the `DOCKER_BUILDKIT=1` environment
variable, e.g.

```bash
DOCKER_BUILDKIT=1 docker build . -t my-custom-runtime:0.1.0
```
````
