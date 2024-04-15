# This is the Striveworks fork of the MLServer Huggingface Chariot Runtime
This allows us to make quickly changes, updates and bug fixes to mlserver hugginface at our own discretion.

## Deploying a new version 
 Once a change is merged and we want to release that change in to chariot there is a process to do so.

First, increment the version within our MLServer Huggingface fork, [example](https://github.com/Striveworks/MLServer/commit/ae550a53bd7f2d1dbffb2d15d61a4c1c3ad29dd3). The switch into to the runtimes/huggingface directory, and run `poetry build`, to build the package. Next we want to push this new version from to our code artifact, if you have already ran ~/chariot/tools/setup-dev, you should be logged into codeartifact.
Run `poetry publish --repository=codeartifact` to publish the new package do code artfiact.

Now we need to update mlserver chariot to use this updated package. Switch to the chariot repo and make a new branch, swith into the mlserver chariot directory (which is at /chariot/py/apps/mlserver-chariot/). The run `poetry add mlserver-huggingface==x.xx` with x.xx set to the new version you created, this will update to pyproject.toml and lock file, go ahead and create and merge a pr with this change, [example](https://github.com/Striveworks/chariot/pull/6321/files).

From then on builds of MLServer chariot will contain your changes. As we attempt to build it daily from main, you can either wait, or if you need it immediately, you can find build your PR generated, https://us-east-2.console.aws.amazon.com/ecr/repositories/private/724664234782/library/chariot-mlserver-chariot?region=us-east-2, and label it with main. Alterntaively you could just kick off new build of MLServer chariot with github actions, and check deploy to dev.


# HuggingFace runtime for MLServer

This package provides a MLServer runtime compatible with HuggingFace Transformers.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-huggingface
```

For further information on how to use MLServer with HuggingFace, you can check
out this [worked out example](../../docs/examples/huggingface/README.md).

## Content Types

The HuggingFace runtime will always decode the input request using its own
built-in codec.
Therefore, [content type annotations](../../docs/user-guide/content-type) at
the request level will **be ignored**.
Note that this **doesn't include [input-level content
type](../../docs/user-guide/content-type#Codecs) annotations**, which will be
respected as usual.

## Settings

The HuggingFace runtime exposes a couple extra parameters which can be used to
customise how the runtime behaves.
These settings can be added under the `parameters.extra` section of your
`model-settings.json` file, e.g.

```{code-block} json
---
emphasize-lines: 5-8
---
{
  "name": "qa",
  "implementation": "mlserver_huggingface.HuggingFaceRuntime",
  "parameters": {
    "extra": {
      "task": "question-answering",
      "optimum_model": true
    }
  }
}
```

````{note}
These settings can also be injected through environment variables prefixed with `MLSERVER_MODEL_HUGGINGFACE_`, e.g.

```bash
MLSERVER_MODEL_HUGGINGFACE_TASK="question-answering"
MLSERVER_MODEL_HUGGINGFACE_OPTIMUM_MODEL=true
```
````

### Loading models
#### Local models
It is possible to load a local model into a HuggingFace pipeline by specifying the model artefact folder path in `parameters.uri` in `model-settings.json`.

#### HuggingFace models
Models in the HuggingFace hub can be loaded by specifying their name in `parameters.extra.pretrained_model` in `model-settings.json`.

````{note}
If `parameters.extra.pretrained_model` is specified, it takes precedence over `parameters.uri`.
````

#### Model Inference
Model inference is done by HuggingFace pipeline. It allows users to run inference on a batch of inputs. Extra inference kwargs can be kept in `parameters.extra`.
```{code-block} json
{
    "inputs": [
        {
            "name": "text_inputs",
            "shape": [1],
            "datatype": "BYTES",
            "data": ["My kitten's name is JoJo,","Tell me a story:"],
        }
    ],
    "parameters": {
        "extra":{"max_new_tokens": 200,"return_full_text": false}
    }
}
```

### Reference

You can find the full reference of the accepted extra settings for the
HuggingFace runtime below:

```{eval-rst}

.. autopydantic_settings:: mlserver_huggingface.settings.HuggingFaceSettings
```
