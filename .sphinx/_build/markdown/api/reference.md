# Python API

MLServer can be installed as a Python package, which exposes a public
framework that can be used to build custom inference runtimes and codecs.

Below, you can find the main reference for the Python API exposed by the
MLServer framework.

* [MLModel](model.md)
* [`mlserver.model`](model.md#module-mlserver.model)
* [Types](types.md)
* [`mlserver.types`](types.md#module-mlserver.types)
* [Codecs](codecs.md)
* [`mlserver.codecs`](codecs.md#module-mlserver.codecs)
* [Metrics](metrics.md)
* [`mlserver.metrics`](metrics.md#module-mlserver.metrics)

## Core Components

The MLServer framework consists of several key components:

### MLModel

The base class for all custom inference runtimes. It exposes the main interface that MLServer will use to interact with ML models.

### Codecs

Handlers for encoding and decoding requests and responses between different content types.

### Types

Core data structures and types used throughout the MLServer framework.

### Metrics

Utilities for collecting and exposing metrics from MLServer instances.

# [`mlserver.model`](#module-mlserver.model)

## Module Contents

# [`mlserver.codecs`](#module-mlserver.codecs)

## Submodules

# [`mlserver.types`](types.md#module-mlserver.types)

## Submodules

# [`mlserver.metrics`](#module-mlserver.metrics)

## Submodules
