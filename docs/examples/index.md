# Examples

To see MLServer in action you can check out the examples below.
These are end-to-end notebooks, showing how to serve models with MLServer.

## Inference Runtimes

If you are interested in how MLServer interacts with particular model
frameworks, you can check the following examples.
These focus on showcasing the different [inference
runtimes](../runtimes/index.md) that ship with MLServer out of the box.
Note that, for **advanced use cases**, you can also write your own custom
inference runtime (see the [example below on custom
models](./custom/README.md)).

- [Serving a `scikit-learn` model](./sklearn/README.md)
- [Serving a `xgboost` model](./xgboost/README.md)
- [Serving a `lightgbm` model](./lightgbm/README.md)
- [Serving a `tempo` pipeline](./tempo/README.md)
- [Serving a `mlflow` model](./mlflow/README.md)
- [Serving a custom model](./custom/README.md)

```{toctree}
:caption: Inference Runtimes
:titlesonly:
:hidden:

Serving a `scikit-learn` model <./sklearn/README.md>
Serving a `xgboost` model <./xgboost/README.md>
Serving a `lightgbm` model <./lightgbm/README.md>
Serving a `tempo` pipeline <./tempo/README.md>
Serving a `mlflow` model <./mlflow/README.md>
Serving a custom model <./custom/README.md>
```

## MLServer Features

To see some of the advanced features included in MLServer (e.g. multi-model
serving), check out the examples below.

- [Multi-Model Serving with multiple frameworks](./mms/README.md)
- [Loading / unloading models from a model repository](./model-repository/README.md)
- [Content-Type Decoding](./content-type/README.md)
- [Custom Conda environment](./conda/README.md)

```{toctree}
:caption: MLServer Features
:titlesonly:
:hidden:

Multi-Model Serving with multiple frameworks <./mms/README.md>
Loading / unloading models from a model repository <./model-repository/README.md>
Content-Type Decoding <./content-type/README.md>
Custom Conda environment <./conda/README.md>
```
