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

### Loading models
#### Local models
It is possible to load a local model into a HuggingFace pipeline by specifying the model artefact folder path in `parameters.uri` in `model-settings.json`.

#### HuggingFace models
Models in the HuggingFace hub can be loaded by specifying their name in `parameters.extra.pretrained_model` in `model-settings.json`.

````{note}
If `parameters.extra.pretrained_model` is specified, it takes precedence over `parameters.uri`.
````

### Reference

You can find the full reference of the accepted extra settings for the
HuggingFace runtime below:

```{eval-rst}

.. autopydantic_settings:: mlserver_huggingface.settings.HuggingFaceSettings
```
