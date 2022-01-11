# LightGBM runtime for MLServer

This package provides a MLServer runtime compatible with LightGBM.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-lightgbm
```

For further information on how to use MLServer with LightGBM, you can check out
this [worked out example](../../docs/examples/lightgbm/README.md).

## Content Types

If no [content type](../../docs/user-guide/content-type) is present on the
request or metadata, the LightGBM runtime will try to decode the payload as
a [NumPy Array](../../docs/user-guide/content-type).
To avoid this, either send a different content type explicitly, or define the
correct one as part of your [model's
metadata](../../docs/reference/model-settings).
