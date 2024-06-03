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

- [Serving Scikit-Learn models](./sklearn/README.md)
- [Serving XGBoost models](./xgboost/README.md)
- [Serving LightGBM models](./lightgbm/README.md)
- [Serving CatBoost models](./catboost/README.md)
- [Serving Tempo pipelines](./tempo/README.md)
- [Serving MLflow models](./mlflow/README.md)
- [Serving custom models](./custom/README.md)
- [Serving Alibi Detect models](./alibi-detect/README.md)
- [Serving HuggingFace models](./huggingface/README.md)

```{toctree}
:caption: Inference Runtimes
:titlesonly:
:hidden:

./sklearn/README.md
./xgboost/README.md
./lightgbm/README.md
./tempo/README.md
./mlflow/README.md
./custom/README.md
./alibi-detect/README.md
./huggingface/README.md
```

## MLServer Features

To see some of the advanced features included in MLServer (e.g. multi-model
serving), check out the examples below.

- [Multi-Model Serving with multiple frameworks](./mms/README.md)
- [Loading / unloading models from a model repository](./model-repository/README.md)
- [Content-Type Decoding](./content-type/README.md)
- [Custom Conda environment](./conda/README.md)
- [Serving custom models requiring JSON inputs or outputs](./custom-json/README.md)
- [Serving models through Kafka](./kafka/README.md)
- [Streaming inference](./streaming/README.md)

```{toctree}
:caption: MLServer Features
:titlesonly:
:hidden:

./mms/README.md
./model-repository/README.md
./content-type/README.md
./conda/README.md
./custom-json/README.md
./kafka/README.md
./streaming/README.md
```

## Tutorials

Tutorials are designed to be *beginner-friendly* and walk through accomplishing a series of tasks using MLServer (and other tools). 

- [Deploying a Custom Tensorflow Model with MLServer and Seldon Core](./cassava/README.md)

```{toctree}
:caption: Tutorials
:titlesonly:
:hidden:

./cassava/README.md
```
