# Content Types

Machine learning models generally expect their inputs to be passed down as a
particular Python type.
Most commonly, this type ranges from _"general purpose"_ NumPy arrays or Pandas
DataFrames to more granular definitions, like `datetime` objects, `Pillow`
images, etc.
Unfortunately, the definition of the [V2 Inference
Protocol](https://kserve.github.io/website/modelserving/inference_api/) doesn't
cover any of the specific use cases.
This protocol can be thought of a wider _"lower level"_ spec, which only
defines what fields a payload should have.

To account for this gap, MLServer introduces support for **content types**,
which offer a way to let MLServer know how it should _"decode"_ V2-compatible
payloads.
When shaped in the right way, these payloads should _"encode"_ all the
information required to extract the higher level Python type that will be
required for a model.

To illustrate the above, we can think of a Scikit-Learn pipeline, which takes
in a Pandas DataFrame and returns a NumPy Array.
Without the use of **content types**, the V2 payload itself would probably lack
information about how this payload should be treated by MLServer
Likewise, the Scikit-Learn pipeline wouldn't know how to treat a raw V2
payload.
In this scenario, the use of content types allows us to specify information on
what's the actual _"higher level"_ information encoded within the V2 protocol
payloads.

![Content Types](../assets/content-type.svg)

## Usage

```{note}
Some inference runtimes may apply a content type by default if none is present.
To learn more about each runtime's defaults, please check the [relevant
inference runtime's docs](../runtimes/index).
```

To let MLServer know that a particular payload must be decoded / encoded as a
different Python data type (e.g. NumPy Array, Pandas DataFrame, etc.), you can
specifity it through the `content_type` field of the `parameters` section of
your request.

As an example, we can consider the following dataframe, containing two columns:
Age and First Name.

| First Name | Age |
| ---------- | --- |
| Joanne     | 34  |
| Michael    | 22  |

This table, could be specified in the V2 protocol as the following payload, where we declare that:

- The whole set of inputs should be decoded as a Pandas Dataframe (i.e. setting
  the content type as `pd`).
- The First Name column should be decoded as a UTF-8 string (i.e. setting the content
  type as `str`).

```{code-block} json
---
emphasize-lines: 2-4, 9-11
---
{
  "parameters": {
    "content_type": "pd"
  },
  "inputs": [
    {
      "name": "First Name",
      "datatype": "BYTES",
      "parameters": {
        "content_type": "str"
      },
      "shape": [2],
      "data": ["Joanne", "Michael"]
    },
    {
      "name": "Age",
      "datatype": "INT32",
      "shape": [2],
      "data": [34, 22]
    },
  ]
}
```

To learn more about the available content types and how to use them, you can
see all the available ones in the [Available Content
Types](#available-content-types) section below.
For a full end-to-end example on how content types work under the hood, you can
also check out this [Content Type Decoding
example](../examples/content-type/README.md).

```{note}
It's important to keep in mind that content types can be specified at both the
**request level** and the **input level**.
The former will apply to the **entire set of inputs**, whereas the latter will
only apply to a **particular input** of the payload.
```

### Model Metadata

Content types can also be defined as part of the [model's
metadata](../reference/model-settings).
This lets the user pre-configure what content types should a model use by
default to decode / encode its requests / responses, without the need to
specify it on each request.

For example, to configure the content type values of the [example
above](#usage), one could create a `model-settings.json` file like the one
below:

```{code-block} json
---
emphasize-lines: 2-4, 9-11
caption: model-settings.json
---
{
  "parameters": {
    "content_type": "pd"
  },
  "inputs": [
    {
      "name": "First Name",
      "datatype": "BYTES",
      "parameters": {
        "content_type": "str"
      },
      "shape": [-1],
    },
    {
      "name": "Age",
      "datatype": "INT32",
      "shape": [-1],
    },
  ]
}
```

It's important to keep in mind that content types passed explicitly as part of
the request will always **take precedence over the model's metadata**.
Therefore, we can leverage this to override the model's metadata when needed.

## Available Content Types

Out of the box, MLServer supports the following list of content types.
However, this can be extended through the use of 3rd-party or custom runtimes.

| Python Type                           | Content Type | Request Level | Input Level |
| ------------------------------------- | ------------ | ------------- | ----------- |
| [NumPy Array](#numpy-array)           | `np`         | ✅            | ✅          |
| [Pandas DataFrame](#pandas-dataframe) | `pd`         | ✅            | ❌          |
| [UTF-8 String](#utf-8-string)         | `str`        | ✅            | ✅          |
| [Base64](#base64)                     | `base64`     | ✅            | ❌          |
| [Datetime](#datetime)                 | `datetime`   | ✅            | ❌          |

```{note}
MLServer allows you extend the supported content types by **adding custom
ones**.
To learn more about how to write your own custom content types, you can check
this [full end-to-end example](../examples/content-type/README.md).
You can also learn more about building custom extensions for MLServer on the
[Custom Inference Runtime section](../runtimes/custom) of the docs.
```

### NumPy Array

```{note}
The [V2 Inference
Protocol](https://kserve.github.io/website/modelserving/inference_api/) expects
that the `data` of each input is sent as a **flat array**.
Therefore, the `np` content type will expect that tensors are sent flattened.
The information in the `shape` field will then be used to reshape the vector
into the right dimensions.
```

The `np` content type will decode / encode V2 payloads to a NumPy Array, taking
into account the following:

- The `datatype` field will be matched to the closest [NumPy
  `dtype`](https://numpy.org/doc/stable/reference/arrays.dtypes.html).
- The `shape` field will be used to reshape the flattened array expected by the
  V2 protocol into the expected tensor shape.

For example, if we think of the following NumPy Array:

```python
import numpy as np

foo = np.array([[1, 2], [3, 4]])
```

We could encode it as the input `foo` in a V2 protocol request as:

```{code-block} json
---
emphasize-lines: 8-10
---
{
  "inputs": [
    {
      "name": "foo",
      "parameters": {
        "content_type": "np"
      },
      "data": [1, 2, 3, 4]
      "datatype": "INT32",
      "shape": [2, 2],
    }
  ]
}
```

When using the NumPy Array content type at the **request-level**, it will decode
the entire request by considering only the first `input` element.
This can be used as a helper for models which only expect a single tensor.

### Pandas DataFrame

```{note}
The `pd` content type can be _stacked_ with other content types.
This allows the user to use a different set of content types to decode each of
the columns.
```

The `pd` content type will decode / encode a V2 request into a Pandas
DataFrame.
For this, it will expect that the DataFrame is shaped in a **columnar way**.
That is,

- Each entry of the `inputs` list (or `outputs`, in the case of
  responses), will represent a column of the DataFrame.
- Each of these entires, will contain all the row elements for that particular
  column.
- The `shape` field of each `input` (or `output`) entry will contain (at least)
  the amount of rows included in the dataframe.

For example, if we consider the following dataframe:

| A   | B   | C   |
| --- | --- | --- |
| a1  | b1  | c1  |
| a2  | b2  | c2  |
| a3  | b3  | c3  |
| a4  | b4  | c4  |

We could encode it to the V2 Inference Protocol as the following payload:

```{code-block} json
---
emphasize-lines: 3, 7-8, 13-14, 19-20
---
{
  "parameters": {
    "content_type": "pd"
  },
  "inputs": [
    {
      "name": "A",
      "data": ["a1", "a2", "a3", "a4"]
      "datatype": "BYTES",
      "shape": [3],
    },
    {
      "name": "B",
      "data": ["b1", "b2", "b3", "b4"]
      "datatype": "BYTES",
      "shape": [3],
    },
    {
      "name": "C",
      "data": ["c1", "c2", "c3", "c4"]
      "datatype": "BYTES",
      "shape": [3],
    },
  ]
}
```

### UTF-8 String

The `str` content type lets you encode / decode a V2 input into a UTF-8
Python string, taking into account the following:

- The expected `datatype` is `BYTES`.
- The `shape` field represents the number of "strings" that are encoded in
  the payload (e.g. the `["hello world", "one more time"]` payload will have a
  shape of 2 elements).

When using the `str` content type at the request-level, it will decode the
entire request by considering only the first `input` element.
This can be used as a helper for models which only expect a single string or a
set of strings.

### Base64

The `base64` content type will decode a binary V2 payload into a Base64-encoded
string (and viceversa), taking into account the following:

- The expected `datatype` is `BYTES`.
- The `data` field should contain the base64-encoded binary strings.
- The `shape` field represents the number of binary strings that are encoded in
  the payload.

For example, if we think of the following _"bytes array"_:

```python
foo = b"Python is fun"
```

We could encode it as the input `foo` of a V2 request as:

```{code-block} json
---
emphasize-lines: 8-10
---
{
  "inputs": [
    {
      "name": "foo",
      "parameters": {
        "content_type": "base64"
      },
      "data": ["UHl0aG9uIGlzIGZ1bg=="]
      "datatype": "BYTES",
      "shape": [1],
    }
  ]
}
```

### Datetime

The `datetime` content type will decode a V2 input into a [Python
`datetime.datetime`
object](https://docs.python.org/3/library/datetime.html#datetime.datetime),
taking into account the following:

- The expected `datatype` is `BYTES`.
- The `data` field should contain the dates serialised following the [ISO 8601
  standard](https://en.wikipedia.org/wiki/ISO_8601).
- The `shape` field represents the number of datetimes that are encoded in
  the payload.

For example, if we think of the following `datetime` object:

```python
import datetime

foo = datetime.datetime(2022, 1, 11, 11, 0, 0)
```

We could encode it as the input `foo` of a V2 request as:

```{code-block} json
---
emphasize-lines: 8-10
---
{
  "inputs": [
    {
      "name": "foo",
      "parameters": {
        "content_type": "datetime"
      },
      "data": ["2022-01-11T11:00:00"]
      "datatype": "BYTES",
      "shape": [1],
    }
  ]
}
```
