# API Reference Overview

This page links to the key reference docs for configuring and using MLServer.

## MLServer Settings

Server-wide configuration (e.g., HTTP/GRPC ports) loaded from a `settings.json` in the working directory. Settings can also be provided via environment variables prefixed with `MLSERVER_` (e.g., `MLSERVER_GRPC_PORT`).

- Scope: server-wide (independent from model-specific settings)
- Sources: `settings.json` or env vars `MLSERVER_*`

[Read the full reference →](./Settings.md)

## Model Settings

Each model has its own configuration (metadata, parallelism, etc.). Typically provided via a `model-settings.json` next to the model artifacts. Alternatively, use env vars prefixed with `MLSERVER_MODEL_` (e.g., `MLSERVER_MODEL_IMPLEMENTATION`). If no `model-settings.json` is found, MLServer will try to load a default model from these env vars. Note: these env vars are shared across models unless overridden by `model-settings.json`.

- Scope: per-model
- Sources: `model-settings.json` or env vars `MLSERVER_MODEL_*`

[Read the full reference →](./ModelSettings.md)

## MLServer CLI

The `mlserver` CLI helps with common model lifecycle tasks (build images, init projects, start serving, etc.). For a quick overview:

```bash
mlserver --help
```

- Commands include: `build`, `dockerfile`, `infer` (deprecated), `init`, `start`
- Each command lists its options, arguments, and examples

[Read the full CLI reference →](./CLI.md)

## Python API

Build custom runtimes and integrate with MLServer using Python:

- MLModel: base class for custom inference runtimes
- Types: request/response schemas and enums (Pydantic)
- Codecs: payload conversions between protocol types and Python types
- Metrics: emit and configure metrics

[Browse the Python API →](./PythonAPI.md)