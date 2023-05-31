# HuggingFace runtime for MLServer

This package provides a MLServer runtime compatible with HuggingFace Transformers.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-huggingface
```

For further information on how to use MLServer with HuggingFace, you can check
out this [worked out example](../../docs/examples/huggingface/README.md).

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

### Reference

You can find the full reference of the accepted extra settings for the
HuggingFace runtime below:

```{eval-rst}

.. autopydantic_settings:: mlserver_huggingface.settings.HuggingFaceSettings
```
