# Inference Runtimes

Inference runtimes allow you to define how your model should be used within
MLServer.
You can think of them as the **backend glue** between MLServer and your machine
learning framework of choice.

![](../assets/architecture.svg)

Out of the box, MLServer comes with a set of pre-packaged runtimes which let
you interact with a subset of common ML frameworks.
This allows you to start serving models saved in these frameworks straight
away.
To avoid bringing in dependencies for frameworks that you don't need to use,
these runtimes are implemented as independent (and optional) Python packages.
This mechanism also allows you to **rollout your [own custom runtimes](./custom)
very easily**.

To pick which runtime you want to use for your model, you just need to make
sure that the right package is installed, and then point to the correct runtime
class in your `model-settings.json` file.

## Included Inference Runtimes

| Framework    | Package Name            | Implementation Class                       | Example                                                    | Documentation                                                    |
| ------------ | ----------------------- | ------------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| Scikit-Learn | `mlserver-sklearn`      | `mlserver_sklearn.SKLearnModel`            | [Scikit-Learn example](../examples/sklearn/README.md)      | [MLServer SKLearn](./sklearn)                                    |
| XGBoost      | `mlserver-xgboost`      | `mlserver_xgboost.XGBoostModel`            | [XGBoost example](../examples/xgboost/README.md)           | [MLServer XGBoost](./xgboost)                                    |
| HuggingFace  | `mlserver-huggingface`  | `mlserver_huggingface.HuggingFaceRuntime`  | [HuggingFace example](../examples/huggingface/README.md)   | [MLServer HuggingFace](./huggingface)                                    |
| Spark MLlib  | `mlserver-mllib`        | `mlserver_mllib.MLlibModel`                | Coming Soon                                                | [MLServer MLlib](./mllib)                                        |
| LightGBM     | `mlserver-lightgbm`     | `mlserver_lightgbm.LightGBMModel`          | [LightGBM example](../examples/lightgbm/README.md)         | [MLServer LightGBM](./lightgbm)                                  |
| Tempo        | `tempo`                 | `tempo.mlserver.InferenceRuntime`          | [Tempo example](../examples/tempo/README.md)               | [`github.com/SeldonIO/tempo`](https://github.com/SeldonIO/tempo) |
| MLflow       | `mlserver-mlflow`       | `mlserver_mlflow.MLflowRuntime`            | [MLflow example](../examples/mlflow/README.md)             | [MLServer MLflow](./mlflow)                                      |
| Alibi-Detect | `mlserver-alibi-detect` | `mlserver_alibi_detect.AlibiDetectRuntime` | [Alibi-detect example](../examples/alibi-detect/README.md) | [MLServer Alibi-Detect](./alibi-detect)                          |

```{toctree}
:hidden:
:titlesonly:

SKLearn <./sklearn>
XGBoost <./xgboost>
MLflow <./mlflow>
Tempo <https://tempo.readthedocs.io>
Spark MLlib <./mllib>
LightGBM <./lightgbm>
Alibi-Detect <./alibi-detect>
HuggingFace <./huggingface>
Custom <./custom>
```
