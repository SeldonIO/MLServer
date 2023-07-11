# MLServer

An open source inference server for your machine learning models.

[![video_play_icon](https://user-images.githubusercontent.com/10466106/151803854-75d17c32-541c-4eee-b589-d45b07ea486d.png)](https://www.youtube.com/watch?v=aZHe3z-8C_w)

## Overview

MLServer aims to provide an easy way to start serving your machine learning
models through a REST and gRPC interface, fully compliant with [KFServing's V2
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

Note that to use any of the optional [inference runtimes](#inference-runtimes),
you'll need to install the relevant package.
For example, to serve a `scikit-learn` model, you would need to install the
`mlserver-sklearn` package:

```bash
pip install mlserver-sklearn
```

For further information on how to use MLServer, you can check any of the
[available examples](#examples).

## Inference Runtimes

Inference runtimes allow you to define how your model should be used within
MLServer.
You can think of them as the **backend glue** between MLServer and your machine
learning framework of choice.
You can read more about [inference runtimes in their documentation
page](./docs/runtimes/index.md).

Out of the box, MLServer comes with a set of pre-packaged runtimes which let
you interact with a subset of common frameworks.
This allows you to start serving models saved in these frameworks straight
away.
However, it's also possible to **[write custom
runtimes](./docs/runtimes/custom.md)**.

Out of the box, MLServer provides support for:

| Framework     | Supported | Documentation                                                    |
| ------------- | --------- | ---------------------------------------------------------------- |
| Scikit-Learn  | ✅        | [MLServer SKLearn](./runtimes/sklearn)                           |
| XGBoost       | ✅        | [MLServer XGBoost](./runtimes/xgboost)                           |
| Spark MLlib   | ✅        | [MLServer MLlib](./runtimes/mllib)                               |
| LightGBM      | ✅        | [MLServer LightGBM](./runtimes/lightgbm)                         |
| Tempo         | ✅        | [`github.com/SeldonIO/tempo`](https://github.com/SeldonIO/tempo) |
| MLflow        | ✅        | [MLServer MLflow](./runtimes/mlflow)                             |
| Alibi-Detect  | ✅        | [MLServer Alibi Detect](./runtimes/alibi-detect)                 |
| Alibi-Explain | ✅        | [MLServer Alibi Explain](./runtimes/alibi-explain)               |
| HuggingFace   | ✅        | [MLServer HuggingFace](./runtimes/huggingface)                   |

## Examples

To see MLServer in action, check out [our full list of
examples](./docs/examples/index.md).
You can find below a few selected examples showcasing how you can leverage
MLServer to start serving your machine learning models.

- [Serving a `scikit-learn` model](./docs/examples/sklearn/README.md)
- [Serving a `xgboost` model](./docs/examples/xgboost/README.md)
- [Serving a `lightgbm` model](./docs/examples/lightgbm/README.md)
- [Serving a `tempo` pipeline](./docs/examples/tempo/README.md)
- [Serving a custom model](./docs/examples/custom/README.md)
- [Serving an `alibi-detect` model](./docs/examples/alibi-detect/README.md)
- [Serving a `HuggingFace` model](./docs/examples/huggingface/README.md)
- [Multi-Model Serving with multiple frameworks](./docs/examples/mms/README.md)
- [Loading / unloading models from a model repository](./docs/examples/model-repository/README.md)

## Developer Guide

### Versioning

Both the main `mlserver` package and the [inference runtimes
packages](./docs/runtimes/index.md) try to follow the same versioning schema.
To bump the version across all of them, you can use the
[`./hack/update-version.sh`](./hack/update-version.sh) script.

For example:

```bash
./hack/update-version.sh 0.2.0.dev1
```
