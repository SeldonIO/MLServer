# XGBoost runtime for MLServer

This package provides a MLServer runtime compatible with XGBoost.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-xgboost
```

For further information on how to use MLServer with XGBoost, you can check out
this [worked out example](../../docs/examples/xgboost/README.md).

## XGBoost Artifact Type

The XGBoost inference runtime will expect that your model is serialised via one
of the following methods:

| Extension | Docs                                                                                                                 | Example                            |
| --------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `*.json`  | [JSON Format](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html#introduction-to-model-io)         | `booster.save_model("model.json")` |
| `*.ubj`   | [Binary JSON Format](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html#introduction-to-model-io)  | `booster.save_model("model.ubj")`  |
| `*.bst`   | [(Old) Binary Format](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html#introduction-to-model-io) | `booster.save_model("model.bst")`  |

````{note}
By default, the runtime will look for a file called `model.[json | ubj | bst]`.
However, this can be modified through the `parameters.uri` field of your
{class}`ModelSettings <mlserver.settings.ModelSettings>` config (see the
section on [Model Settings](../../docs/reference/model-settings.md) for more
details).

```{code-block} json
---
emphasize-lines: 3-5
---
{
  "name": "foo",
  "parameters": {
    "uri": "./my-own-model-filename.json"
  }
}
```
````

## Content Types

If no [content type](../../docs/user-guide/content-type) is present on the
request or metadata, the XGBoost runtime will try to decode the payload as a
[NumPy Array](../../docs/user-guide/content-type).
To avoid this, either send a different content type explicitly, or define the
correct one as part of your [model's
metadata](../../docs/reference/model-settings).

## Model Outputs

The XGBoost inference runtime exposes a number of outputs depending on the
model type.
These outputs match to the `predict` and `predict_proba` methods of the XGBoost
model.

| Output          | Returned By Default | Availability                                                          |
| --------------- | ------------------- | --------------------------------------------------------------------- |
| `predict`       | ✅                  | Available on all XGBoost models.                                      |
| `predict_proba` | ❌                  | Only available on non-regressor models (i.e. `XGBClassifier` models). |

By default, the runtime will only return the output of `predict`.
However, you are able to control which outputs you want back through the
`outputs` field of your {class}`InferenceRequest
<mlserver.types.InferenceRequest>` payload.

For example, to only return the model's `predict_proba` output, you could
define a payload such as:

```{code-block} json
---
emphasize-lines: 10-12
---
{
  "inputs": [
    {
      "name": "my-input",
      "datatype": "INT32",
      "shape": [2, 2],
      "data": [1, 2, 3, 4]
    }
  ],
  "outputs": [
    { "name": "predict_proba" }
  ]
}
```
