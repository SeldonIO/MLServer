# Examples

To see MLServer in action you can check out the examples below.
These are end-to-end notebooks, showing how to serve models with MLServer.

## Inference Runtimes

If you are interested in how MLServer interacts with particular model
frameworks, you can check the following examples.
These focus on showcasing the different [inference
runtimes](../runtimes/index.md) that ship with MLServer out of the box.
Note that, for advanced use cases, you can also write your own custom inference
runtime.

- [Serving a `scikit-learn` model](./docs/examples/sklearn/README.md)
- [Serving a `xgboost` model](./docs/examples/xgboost/README.md)
- [Serving a `lightgbm` model](./docs/examples/lightgbm/README.md)
- [Serving a `tempo` pipeline](./docs/examples/tempo/README.md)
- [Serving a `mlflow` model](./docs/examples/mlflow/README.md)
- [Serving a custom model](./docs/examples/custom/README.md)

## MLServer Features

To see some of the advanced features included in MLServer (e.g. multi-model
serving), check out the examples below.

- [Multi-Model Serving with multiple frameworks](./docs/examples/mms/README.md)
- [Loading / unloading models from a model repository](./docs/examples/model-repository/README.md)
- [Content-Type Decoding](./docs/examples/content-type/README.md)
- [Custom Conda environment](./docs/examples/conda/README.md)
