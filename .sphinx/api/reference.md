# Python API

MLServer can be installed as a Python package, which exposes a public
framework that can be used to build custom inference runtimes and codecs.

Below, you can find the main reference for the Python API exposed by the
MLServer framework.

```{toctree}
:titlesonly:

./model.md
./types.md
./codecs.md
./metrics.md
```

## Core Components

The MLServer framework consists of several key components:

### MLModel

The base class for all custom inference runtimes. It exposes the main interface that MLServer will use to interact with ML models.

```{autodoc2-object} mlserver.model
:renderer: myst
```

### Codecs

Handlers for encoding and decoding requests and responses between different content types.

```{autodoc2-object} mlserver.codecs
:renderer: myst
```

### Types

Core data structures and types used throughout the MLServer framework.

```{autodoc2-object} mlserver.types
:renderer: myst
```

### Metrics

Utilities for collecting and exposing metrics from MLServer instances.

```{autodoc2-object} mlserver.metrics
:renderer: myst
``` 