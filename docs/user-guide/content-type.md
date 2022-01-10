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
defines what fields should a payload have.

To account for this gap, MLServer introduces support for **content types**,
which offer a way to let MLServer know how it should _"decode"_ V2-compatible
payloads.
When shaped in the right way, these payloads should _"encode"_ all the
information required to extract the higher level Python type that will be
required for a model.

To illustrate the above, we can think of a Scikit-Learn pipeline, which takes
in a Pandas DataFrame and returns a NumPy Array.
Without the use of **content types**, the V2 payload itself would probably lack
information about how should this payload be treated by MLServer.
Likewise, the Scikit-Learn pipeline wouldn't know how to treat a raw V2
payload.
In this scenario, the use of content types allows us to specify information on
what's the actual _"higher level"_ information encoded within the V2 protocol
payloads.

![Content Types](../assets/content-type.svg)

## Usage

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
- The Age column should be decoded as a UTF-8 string (i.e. setting the content
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

```{note}
It's important to keep in mind that content types can be specified at both the
**request level** and the **input level**.
The former will apply to the **entire set of inputs**, whereas the latter will
only apply to a **particular input** of the payload.
```

## Available Content Types

Out of the box, MLServer supports the following list of content types.
However, this can be extended through the use of 3rd-party or custom runtimes.

| Python Type                           | Content Type | Request Level | Input Level |
| ------------------------------------- | ------------ | ------------- | ----------- |
| [NumPy Array](#numpy-array)           | `np`         | 👍            | 👍          |
| [Pandas DataFrame](#pandas-dataframe) | `pd`         | 👍            | ❌          |
| UTF-8 String                          | `str`        | 👍            | 👍          |
| Base64 Binary Payload                 | `base64`     | 👍            | 👍          |
| Datetime                              | `datetime`   | 👍            | 👍          |

### NumPy Array

The `np` content type will decode / encode V2 payloads to a NumPy Array, taking
into account the following:

- The `datatype` field will be matched to the closest [NumPy
  `dtype`](https://numpy.org/doc/stable/reference/arrays.dtypes.html).
- The `shape` field will be used to reshape the flattened array expected by the
  V2 protocol into the expected tensor shape.

When using the NumPy Array at the request-level, it will decode the entire
request by considering only the first `input` element.
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
