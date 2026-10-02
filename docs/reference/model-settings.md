# Model Settings

In MLServer, each loaded model can be configured separately.
This configuration will include model information (e.g. metadata about the
accepted inputs), but also model-specific settings (e.g. number of [parallel
workers](../user-guide/parallel-inference) to run inference).

This configuration will usually be provided through a `model-settings.json`
file which **sits next to the model artifacts**.
However, it's also possible to provide this through environment variables
prefixed with `MLSERVER_MODEL_` (e.g. `MLSERVER_MODEL_IMPLEMENTATION`). Note
that, in the latter case, this environment variables will be shared across all
loaded models (unless they get overriden by a `model-settings.json` file).
Additionally, if no `model-settings.json` file is found, MLServer will also try
to load a _"default"_ model from these environment variables.

Before registering a model, MLServer checks that its name is neither empty nor
entirely whitespace. When loading a `model-settings.json` file, a missing or empty
`name` defaults to the name of the containing folder. When configuring a model
only through environment variables, set `MLSERVER_MODEL_NAME` to a non-empty name.
Models created programmatically must also have a non-empty name before they are
loaded into the registry.

## Settings

```{eval-rst}

.. autopydantic_settings:: mlserver.settings.ModelSettings
```

## Extra Model Parameters

```{eval-rst}

.. autopydantic_settings:: mlserver.settings.ModelParameters
```
