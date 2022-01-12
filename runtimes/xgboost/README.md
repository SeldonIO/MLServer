# XGBoost runtime for MLServer

This package provides a MLServer runtime compatible with XGBoost.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-xgboost
```

For further information on how to use MLServer with XGBoost, you can check out
this [worked out example](../../docs/examples/xgboost/README.md).

## Content Types

The XGBoost runtime supports a new `dmatrix` content type, aim to decode V2
Inference payloads into [XGBoost's `DMatrix` data
type](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.DMatrix).
This content type uses a similar set of encoding rules as the [NumPy Array
one](../../docs/user-guide/content-type).

If no content type is specified on either the request payload or the model's
metadata, the XGBoost runtime will default to the `dmatrix` content type.
To avoid this, either send a different content type explicitly, or define the
correct one as part of your [model's
metadata](../../docs/reference/model-settings).
