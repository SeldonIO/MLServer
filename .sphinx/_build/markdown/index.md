# MLServer

An open source inference server for your machine learning models.

[![video_play_icon](https://user-images.githubusercontent.com/10466106/151803854-75d17c32-541c-4eee-b589-d45b07ea486d.png)](https://www.youtube.com/watch?v=aZHe3z-8C_w)

## Overview

MLServer aims to provide an easy way to start serving your machine learning
models through a REST and gRPC interface, fully compliant with [KFServing’s V2
Dataplane](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html)
spec. Watch a quick video introducing the project [here](https://www.youtube.com/watch?v=aZHe3z-8C_w).

- Multi-model serving, letting users run multiple models within the same
  process.
- Ability to run [inference in parallel for vertical
  scaling](https://mlserver.readthedocs.io/en/latest/user-guide/parallel-inference.html)
  across multiple models through a pool of inference workers.
- Support for [adaptive
  batching](https://mlserver.readthedocs.io/en/latest/user-guide/adaptive-batching.html),
  to group inference requests together on the fly.
- Scalability with deployment in Kubernetes native frameworks, including
  [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/graph/protocols.html#v2-kfserving-protocol) and
  [KServe (formerly known as KFServing)](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/), where
  MLServer is the core Python inference server used to serve machine learning
  models.
- Support for the standard [V2 Inference Protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html) on
  both the gRPC and REST flavours, which has been standardised and adopted by
  various model serving frameworks.

You can read more about the goals of this project on the [initial design
document](https://docs.google.com/document/d/1C2uf4SaAtwLTlBCciOhvdiKQ2Eay4U72VxAD4bXe7iU/edit?usp=sharing).

## Usage

You can install the `mlserver` package running:

```bash
pip install mlserver
```

Note that to use any of the optional [inference runtimes](),
you’ll need to install the relevant package.
For example, to serve a `scikit-learn` model, you would need to install the
`mlserver-sklearn` package:

```bash
pip install mlserver-sklearn
```

For further information on how to use MLServer, you can check any of the
[available examples]().

## Inference Runtimes

Inference runtimes allow you to define how your model should be used within
MLServer.
You can think of them as the **backend glue** between MLServer and your machine
learning framework of choice.
You can read more about inference runtimes in their documentation
page.

Out of the box, MLServer comes with a set of pre-packaged runtimes which let
you interact with a subset of common frameworks.
This allows you to start serving models saved in these frameworks straight
away.
However, it’s also possible to **write custom
runtimes**.

Out of the box, MLServer provides support for:

| Framework     | Supported   | Documentation                                                    |
|---------------|-------------|------------------------------------------------------------------|
| Scikit-Learn  | ✅          | [MLServer SKLearn]()                                             |
| XGBoost       | ✅          | [MLServer XGBoost]()                                             |
| Spark MLlib   | ✅          | [MLServer MLlib]()                                               |
| LightGBM      | ✅          | [MLServer LightGBM]()                                            |
| CatBoost      | ✅          | [MLServer CatBoost]()                                            |
| Tempo         | ✅          | [`github.com/SeldonIO/tempo`](https://github.com/SeldonIO/tempo) |
| MLflow        | ✅          | [MLServer MLflow]()                                              |
| Alibi-Detect  | ✅          | [MLServer Alibi Detect]()                                        |
| Alibi-Explain | ✅          | [MLServer Alibi Explain]()                                       |
| HuggingFace   | ✅          | [MLServer HuggingFace]()                                         |

MLServer is licensed under the Apache License, Version 2.0. However please note that software used in conjunction with, or alongside, MLServer may be licensed under different terms. For example, Alibi Detect and Alibi Explain are both licensed under the Business Source License 1.1. For more information about the legal terms of products that are used in conjunction with or alongside MLServer, please refer to their respective documentation.

## Supported Python Versions

🔴 Unsupported

🟠 Deprecated: To be removed in a future version

🟢 Supported

🔵 Untested

|   Python Version | Status   |
|------------------|----------|
|             3.7  | 🔴       |
|             3.8  | 🔴       |
|             3.9  | 🟢       |
|             3.1  | 🟢       |
|             3.11 | 🟢       |
|             3.12 | 🟢       |
|             3.13 | 🔴       |

## Examples

To see MLServer in action, check out our full list of
examples.
You can find below a few selected examples showcasing how you can leverage
MLServer to start serving your machine learning models.

- Serving a `scikit-learn` model
- Serving a `xgboost` model
- Serving a `lightgbm` model
- Serving a `catboost` model
- Serving a `tempo` pipeline
- Serving a custom model
- Serving an `alibi-detect` model
- Serving a `HuggingFace` model
- Multi-Model Serving with multiple frameworks
- Loading / unloading models from a model repository

## Developer Guide

### Versioning

Both the main `mlserver` package and the inference runtimes
packages try to follow the same versioning schema.
To bump the version across all of them, you can use the
[`./hack/update-version.sh`](../hack/update-version.sh) script.

We generally keep the version as a placeholder for an upcoming version.

For example:

```bash
./hack/update-version.sh 0.2.0.dev1
```

### Testing

To run all of the tests for MLServer and the runtimes, use:

```bash
make test
```

To run run tests for a single file, use something like:

```bash
tox -e py3 -- tests/batch_processing/test_rest.py
```

# MLServer Documentation

Welcome to the MLServer documentation. This documentation is built using Sphinx and optimized for GitBook deployment.

## Quick Links

- [API Reference](api/reference.md) - Complete Python API documentation
- [GitHub Repository](https://github.com/SeldonIO/MLServer/) - Source code and issues
- [Main Documentation](https://mlserver.readthedocs.io/) - Full documentation with guides and examples
