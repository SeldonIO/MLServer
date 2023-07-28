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
Not that this **doesn't include [input-level content
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

### Loading local models
It is possible to load a model from a local path into a HuggingFace pipeline, if desired. 
The path must point to a folder containing the model artefacts compatible with the HuggingFace specifications.
#### Multi-model serving folder structure
In the case of MMS, the example below assumes the desired model folder resides in `./models`, e.g. `./models/your-model-artefacts-folder` and inside a `models-settings.json` file is expected to exist.
The `uri` field could be an absolute path to the model artefacts folder or a relative path to the folder from which MLServer is started.
```{code-block} json
---
emphasize-lines: 5-5
---
{
  "name": "qa",
  "implementation": "mlserver_huggingface.HuggingFaceRuntime",
  "parameters": {
      "uri": "./models/your-model-artefacts-folder",
      "version": "v1.0",
      "extra": {
          "task": "question-answering",
      }
  }
}
```

````{note}
If a `parameters.extra.pretrained_model` parameter is specified in `parameters.extra` section, it will take precedence 
over `parameters.uri`. Furthermore, in the case of MMS, `parameters.extra.pretrained_model` and `parameters.uri` can 
be used interchangeably only if the paths provided are absolute. This is because the `parameters.extra.pretrained_model` 
expects a relative path to itself, i.e. relative to the `model-settings.json`.
````

### Reference

You can find the full reference of the accepted extra settings for the
HuggingFace runtime below:

```{eval-rst}

.. autopydantic_settings:: mlserver_huggingface.settings.HuggingFaceSettings
```
