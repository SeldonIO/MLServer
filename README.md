# MLServer

An open source inference server to serve your machine learning models.

> :warning: **This is a Work in Progress**.

## Overview

MLServer aims to provide an easy way to start serving your machine learning
models through a REST and gRPC interface, fully compliant with [KFServing's V2
Dataplane](https://github.com/kubeflow/kfserving/blob/master/docs/predict-api/v2/required_api.md)
spec.

You can read more about the goals of this project on the [inital design
document](https://docs.google.com/document/d/1C2uf4SaAtwLTlBCciOhvdiKQ2Eay4U72VxAD4bXe7iU/edit?usp=sharing).

## Usage

You can install the `mlserver` package running:

```bash
pip install mlserver
```

Note that to use any of the optional [inference runtimes](#Inference-Runtimes),
you'll need to install the relevant package.
For example, to serve a `scikit-learn` model, you would need to install the
`mlserver-sklearn` package:

```bash
pip install mlserver-sklearn
```

For further information on how to use MLServer, you can check any of the
[available examples](#Examples).

## Inference Runtimes

Inference runtimes allow you to define how your model should be used within
MLServer.
Out of the box, MLServer comes with a set of pre-packaged runtimes which let
you interact with a subset of common ML frameworks.
This allows you to start serving models saved in these frameworks straight
away.

To avoid bringing in dependencies for frameworks that you don't need to use,
these runtimes are implemented as independent optional packages.
This mechanism also allows you to rollout your [own custom runtimes]( very easily.

To pick which runtime you want to use for your model, you just need to make
sure that the right package is installed, and then point to the correct runtime
class in your `model-settings.json` file.

The included runtimes are:

| Framework    | Package Name       | Implementation Class            | Example                                              | Source Code                                |
| ------------ | ------------------ | ------------------------------- | ---------------------------------------------------- | ------------------------------------------ |
| Scikit-Learn | `mlserver-sklearn` | `mlserver_sklearn.SKLearnModel` | [Scikit-Learn example](./examples/sklearn/README.md) | [`./runtimes/sklearn`](./runtimes/sklearn) |
| XGBoost      | `mlserver-xgboost` | `mlserver_xgboost.XGBoostModel` | [XGBoost example](./examples/xgboost/README.md)      | [`./runtimes/xgboost`](./runtimes/xgboost) |
| Spark MLlib  | `mlserver-mllib`   | `mlserver_mllib.MLlibModel`     | Coming Soon                                          | [`./runtimes/mllib`](./runtimes/mllib)     |
| LightGBM | `mlserver-lightgbm`   | `mlserver_lightgbm.LightGBMModel`     | Coming Soon                                          | [`./runtimes/lightgbm`](./runtimes/lightgbm)   |
| Tempo | `mlserver-tempo`   | `mlserver_tempo.TempoModel`     | [Tempo example](./examples/tempo/README.md)                                          | [`./runtimes/tempo`](./runtimes/tempo)   |

## Examples

On the list below, you can find a few examples on how you can leverage
`mlserver` to start serving your machine learning models.

- [Serving a `scikit-learn` model](./examples/sklearn/README.md)
- [Serving a `xgboost` model](./examples/xgboost/README.md)
- [Serving a `lightgbm` model](./examples/lightgbm/README.md)
- [Serving a `tempo` pipeline](./examples/tempo/README.md)
- [Serving a custom model](./examples/custom/README.md)
- [Multi-Model Serving with multiple frameworks](./examples/mms/README.md)
- [Loading / unloading models from a model repository](./examples/model-repository/README.md)

## Developer Guide

### Versioning

Both the main `mlserver` package and the [inference runtimes
packages](./runtimes) try to follow the same versioning schema.
To bump the version across all of them, you can use the
[`./hack/update-version.sh`](./hack/update-version.sh) script.
For example:

```bash
./hack/update-version.sh 0.2.0.dev1
```
