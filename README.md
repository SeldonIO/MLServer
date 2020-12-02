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

## Runtimes

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

## Examples

On the list below, you can find a few examples on how you can leverage
`mlserver` to start serving your machine learning models.

- [Serving a `scikit-learn` model](./examples/sklearn/README.md)
- [Serving a `xgboost` model](./examples/xgboost/README.md)
- [Serving a custom model](./examples/custom/README.md)
- [Multi-Model Serving with multiple frameworks](./examples/mms/README.md)
- [Loading / unloading models from a model repository](./examples/model-repository/README.md)
