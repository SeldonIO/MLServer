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

## Examples

On the list below, you can find a few examples on how you can leverage
`mlserver` to start serving your machine learning models.

- [Serving a `scikit-learn` model](./examples/sklearn/README.md)
- [Serving a `xgboost` model](./examples/xgboost/README.md)
- [Serving a custom model](./examples/custom/README.md)
- [Multi-Model Serving with multiple frameworks](./examples/mms/README.md)
- [Loading / unloading models from a model repository](./examples/model-repository/README.md)
