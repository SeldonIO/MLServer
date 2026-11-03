# CatBoost runtime for MLServer

This package provides a MLServer runtime compatible with CatBoost's `CatboostClassifier`.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-catboost
```

For further information on how to use MLServer with CatBoost, you can check out
this [worked out example](../../docs/examples/catboost/README.md).

## Content Types

If no [content type](../../docs/user-guide/content-type) is present on the
request or metadata, the CatBoost runtime will try to decode the payload as
a [NumPy Array](../../docs/user-guide/content-type).
To avoid this, either send a different content type explicitly, or define the
correct one as part of your [model's
metadata](../../docs/reference/model-settings).

## Model outputs

By default the runtime returns class labels as `predict`. To return class
probabilities, set `PREDICT_PROBA=true` in the server environment or set
`parameters.extra.predict_fn` to `predict_proba` in `model-settings.json`.
The probability output has one column per class in the model's class order.

A request can explicitly select `predict`, `predict_proba`, or both through
its `outputs` list. Request outputs take precedence over the model setting,
which takes precedence over `PREDICT_PROBA`. The environment variable applies
to all CatBoost models served by the process.

```json
{
  "outputs": [{"name": "predict_proba"}]
}
```

The request above shows only the `outputs` field; include the usual `inputs`
in an inference request.
