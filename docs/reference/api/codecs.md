# Codecs

Codecs are used to encapsulate the logic required to encode / decode payloads
following the [Open Inference
Protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html)
into high-level Python types.
You can read more about the high-level concepts behind codecs in the
[](../../user-guide/content-type) section of the docs, as well as how to use
them.

## Base Codecs

All the codecs within MLServer extend from either the {class}`InputCodec <mlserver.codecs.base.InputCodec>`
or the {class}`RequestCodec <mlserver.codecs.base.RequestCodec>` base classes.
These define the interface to deal with input (outputs) and request (responses)
respectively.

```{eval-rst}
.. automodule:: mlserver.codecs
   :members: InputCodec, RequestCodec
```

## Built-in Codecs

The `mlserver` package will include a set of built-in codecs to cover common
conversions.
You can learn more about these in the [](../../user-guide/content-type.md#available-content-types) section of
the docs.

```{eval-rst}
.. automodule:: mlserver.codecs
   :members: NumpyCodec, NumpyRequestCodec, StringCodec, StringRequestCodec, Base64Codec, DatetimeCodec, PandasCodec
```
