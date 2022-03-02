# Alibi-Detect runtime for MLServer

This package provides a MLServer runtime compatible with [alibi-detect](https://docs.seldon.io/projects/alibi-detect/en/latest/index.html) models.

## Usage

You can install the runtime, alongside `mlserver`, as:

```bash
pip install mlserver mlserver-alibi-detect
```

For further information on how to use MLServer with Alibi-Detect, you can check
out this [worked out example](../../docs/examples/alibi-detect/README.md).

## Content Types

If no [content type](../../docs/user-guide/content-type) is present on the
request or metadata, the Alibi-Detect runtime will try to decode the payload
as a [NumPy Array](../../docs/user-guide/content-type).
To avoid this, either send a different content type explicitly, or define the
correct one as part of your [model's
metadata](../../docs/reference/model-settings).
