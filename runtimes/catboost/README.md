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
