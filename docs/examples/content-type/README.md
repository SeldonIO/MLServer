# Content Type Decoding

MLServer extends the V2 inference protocol by adding support for a `content_type` annotation.
This annotation can be provided either through the model metadata `parameters`, or through the input `parameters`.
By leveraging the `content_type` annotation, we can provide the necessary information to MLServer so that it can _decode_ the input payload from the "wire" V2 protocol to something meaningful to the model / user (e.g. a NumPy array).

This example will walk you through some examples which illustrate how this works, and how it can be extended.

## Echo Inference Runtime

To start with, we will write a _dummy_ runtime which just prints the input, the _decoded_ input and returns it.
This will serve as a testbed to showcase how the `content_type` support works.

Later on, we will extend this runtime by adding custom _codecs_ that will decode our V2 payload to custom types.


```python
%%writefile runtime.py
import json

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from mlserver.codecs import DecodedParameterName

_to_exclude = {
    "parameters": {DecodedParameterName, "headers"},
    'inputs': {"__all__": {"parameters": {DecodedParameterName, "headers"}}}
}

class EchoRuntime(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        outputs = []
        for request_input in payload.inputs:
            decoded_input = self.decode(request_input)
            print(f"------ Encoded Input ({request_input.name}) ------")
            as_dict = request_input.dict(exclude=_to_exclude)  # type: ignore
            print(json.dumps(as_dict, indent=2))
            print(f"------ Decoded input ({request_input.name}) ------")
            print(decoded_input)

            outputs.append(
                ResponseOutput(
                    name=request_input.name,
                    datatype=request_input.datatype,
                    shape=request_input.shape,
                    data=request_input.data
                )
            )

        return InferenceResponse(model_name=self.name, outputs=outputs)

```

As you can see above, this runtime will decode the incoming payloads by calling the `self.decode()` helper method.
This method will check what's the right content type for each input in the following order:

1. Is there any content type defined in the `inputs[].parameters.content_type` field within the **request payload**?
2. Is there any content type defined in the `inputs[].parameters.content_type` field within the **model metadata**?
3. Is there any default content type that should be assumed?


### Model Settings

In order to enable this runtime, we will also create a `model-settings.json` file.
This file should be present (or accessible from) in the folder where we run `mlserver start .`.


```python
%%writefile model-settings.json

{
    "name": "content-type-example",
    "implementation": "runtime.EchoRuntime"
}
```

## Request Inputs

Our initial step will be to decide the content type based on the incoming `inputs[].parameters` field.
For this, we will start our MLServer in the background (e.g. running `mlserver start .`)


```python
import requests

payload = {
    "inputs": [
        {
            "name": "parameters-np",
            "datatype": "INT32",
            "shape": [2, 2],
            "data": [1, 2, 3, 4],
            "parameters": {
                "content_type": "np"
            }
        },
        {
            "name": "parameters-str",
            "datatype": "BYTES",
            "shape": [1],
            "data": "hello world 😁",
            "parameters": {
                "content_type": "str"
            }
        }
    ]
}

response = requests.post(
    "http://localhost:8080/v2/models/content-type-example/infer",
    json=payload
)
```

### Codecs

As you've probably already noticed, writing request payloads compliant with both the V2 Inference Protocol requires a certain knowledge about both the V2 spec and the structure expected by each content type.
To account for this and simplify usage, the MLServer package exposes a set of utilities which will help you interact with your models via the V2 protocol.

These helpers are mainly shaped as _"codecs"_.
That is, abstractions which know how to _"encode"_ and _"decode"_ arbitrary Python datatypes to and from the V2 Inference Protocol.

Generally, we recommend using the existing set of codecs to generate your V2 payloads.
This will ensure that requests and responses follow the right structure, and should provide a more seamless experience.

Following with our previous example, the same code could be rewritten using codecs as:


```python
import requests
import numpy as np

from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import NumpyCodec, StringCodec

parameters_np = np.array([[1, 2], [3, 4]])
parameters_str = ["hello world 😁"]

payload = InferenceRequest(
    inputs=[
        NumpyCodec.encode_input("parameters-np", parameters_np),
        # The `use_bytes=False` flag will ensure that the encoded payload is JSON-compatible
        StringCodec.encode_input("parameters-str", parameters_str, use_bytes=False),
    ]
)

response = requests.post(
    "http://localhost:8080/v2/models/content-type-example/infer",
    json=payload.dict()
)

response_payload = InferenceResponse.parse_raw(response.text)
print(NumpyCodec.decode_output(response_payload.outputs[0]))
print(StringCodec.decode_output(response_payload.outputs[1]))
```

Note that the rewritten snippet now makes use of the built-in `InferenceRequest` class, which represents a V2 inference request.
On top of that, it also uses the `NumpyCodec` and `StringCodec` implementations, which know how to encode a Numpy array and a list of strings into V2-compatible request inputs.

### Model Metadata

Our next step will be to define the expected content type through the model metadata.
This can be done by extending the `model-settings.json` file, and adding a section on inputs.


```python
%%writefile model-settings.json

{
    "name": "content-type-example",
    "implementation": "runtime.EchoRuntime",
    "inputs": [
        {
            "name": "metadata-np",
            "datatype": "INT32",
            "shape": [2, 2],
            "parameters": {
                "content_type": "np"
            }
        },
        {
            "name": "metadata-str",
            "datatype": "BYTES",
            "shape": [11],
            "parameters": {
                "content_type": "str"
            }
        }
    ]
}
```

After adding this metadata, we will re-start MLServer (e.g. `mlserver start .`) and we will send a new request without any explicit `parameters`.


```python
import requests

payload = {
    "inputs": [
        {
            "name": "metadata-np",
            "datatype": "INT32",
            "shape": [2, 2],
            "data": [1, 2, 3, 4],
        },
        {
            "name": "metadata-str",
            "datatype": "BYTES",
            "shape": [11],
            "data": "hello world 😁",
        }
    ]
}

response = requests.post(
    "http://localhost:8080/v2/models/content-type-example/infer",
    json=payload
)
```

As you should be able to see in the server logs, MLServer will cross-reference the input names against the model metadata to find the right content type.

### Custom Codecs

There may be cases where a custom inference runtime may need to encode / decode to custom datatypes.
As an example, we can think of computer vision models which may only operate with `pillow` image objects.

In these scenarios, it's possible to extend the `Codec` interface to write our custom encoding logic.
A `Codec`, is simply an object which defines a `decode()` and `encode()` methods.
To illustrate how this would work, we will extend our custom runtime to add a custom `PillowCodec`.


```python
%%writefile runtime.py
import io
import json

from PIL import Image

from mlserver import MLModel
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
)
from mlserver.codecs import NumpyCodec, register_input_codec, DecodedParameterName
from mlserver.codecs.utils import InputOrOutput


_to_exclude = {
    "parameters": {DecodedParameterName},
    "inputs": {"__all__": {"parameters": {DecodedParameterName}}},
}


@register_input_codec
class PillowCodec(NumpyCodec):
    ContentType = "img"
    DefaultMode = "L"

    @classmethod
    def can_encode(cls, payload: Image) -> bool:
        return isinstance(payload, Image)

    @classmethod
    def _decode(cls, input_or_output: InputOrOutput) -> Image:
        if input_or_output.datatype != "BYTES":
            # If not bytes, assume it's an array
            image_array = super().decode_input(input_or_output)  # type: ignore
            return Image.fromarray(image_array, mode=cls.DefaultMode)

        encoded = input_or_output.data
        if isinstance(encoded, str):
            encoded = encoded.encode()

        return Image.frombytes(
            mode=cls.DefaultMode, size=input_or_output.shape, data=encoded
        )

    @classmethod
    def encode_output(cls, name: str, payload: Image) -> ResponseOutput:  # type: ignore
        byte_array = io.BytesIO()
        payload.save(byte_array, mode=cls.DefaultMode)

        return ResponseOutput(
            name=name, shape=payload.size, datatype="BYTES", data=byte_array.getvalue()
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> Image:
        return cls._decode(response_output)

    @classmethod
    def encode_input(cls, name: str, payload: Image) -> RequestInput:  # type: ignore
        output = cls.encode_output(name, payload)
        return RequestInput(
            name=output.name,
            shape=output.shape,
            datatype=output.datatype,
            data=output.data,
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> Image:
        return cls._decode(request_input)


class EchoRuntime(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        outputs = []
        for request_input in payload.inputs:
            decoded_input = self.decode(request_input)
            print(f"------ Encoded Input ({request_input.name}) ------")
            as_dict = request_input.dict(exclude=_to_exclude)  # type: ignore
            print(json.dumps(as_dict, indent=2))
            print(f"------ Decoded input ({request_input.name}) ------")
            print(decoded_input)

            outputs.append(
                ResponseOutput(
                    name=request_input.name,
                    datatype=request_input.datatype,
                    shape=request_input.shape,
                    data=request_input.data,
                )
            )

        return InferenceResponse(model_name=self.name, outputs=outputs)
```

We should now be able to restart our instance of MLServer (i.e. with the `mlserver start .` command), to send a few test requests.


```python
import requests

payload = {
    "inputs": [
        {
            "name": "image-int32",
            "datatype": "INT32",
            "shape": [8, 8],
            "data": [
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 0, 1, 0
            ],
            "parameters": {
                "content_type": "img"
            }
        },
        {
            "name": "image-bytes",
            "datatype": "BYTES",
            "shape": [8, 8],
            "data": (
                "10101010"
                "10101010"
                "10101010"
                "10101010"
                "10101010"
                "10101010"
                "10101010"
                "10101010"
            ),
            "parameters": {
                "content_type": "img"
            }
        }
    ]
}

response = requests.post(
    "http://localhost:8080/v2/models/content-type-example/infer",
    json=payload
)
```

As you should be able to see in the MLServer logs, the server is now able to decode the payload into a Pillow image.
This example also illustrates how `Codec` objects can be compatible with multiple `datatype` values (e.g. tensor and `BYTES` in this case).

## Request Codecs

So far, we've seen how you can specify codecs so that they get applied at the input level.
However, it is also possible to use request-wide codecs that aggregate multiple inputs to decode the payload.
This is usually relevant for cases where the models expect a multi-column input type, like a Pandas DataFrame.

To illustrate this, we will first tweak our `EchoRuntime` so that it prints the decoded contents at the request level.


```python
%%writefile runtime.py
import json

from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput
from mlserver.codecs import DecodedParameterName

_to_exclude = {
    "parameters": {DecodedParameterName},
    'inputs': {"__all__": {"parameters": {DecodedParameterName}}}
}

class EchoRuntime(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        print("------ Encoded Input (request) ------")
        as_dict = payload.dict(exclude=_to_exclude)  # type: ignore
        print(json.dumps(as_dict, indent=2))
        print("------ Decoded input (request) ------")
        decoded_request = None
        if payload.parameters:
            decoded_request = getattr(payload.parameters, DecodedParameterName)
        print(decoded_request)

        outputs = []
        for request_input in payload.inputs:
            outputs.append(
                ResponseOutput(
                    name=request_input.name,
                    datatype=request_input.datatype,
                    shape=request_input.shape,
                    data=request_input.data
                )
            )

        return InferenceResponse(model_name=self.name, outputs=outputs)

```

We should now be able to restart our instance of MLServer (i.e. with the `mlserver start .` command), to send a few test requests.


```python
import requests

payload = {
    "inputs": [
        {
            "name": "parameters-np",
            "datatype": "INT32",
            "shape": [2, 2],
            "data": [1, 2, 3, 4],
            "parameters": {
                "content_type": "np"
            }
        },
        {
            "name": "parameters-str",
            "datatype": "BYTES",
            "shape": [2, 11],
            "data": ["hello world 😁", "bye bye 😁"],
            "parameters": {
                "content_type": "str"
            }
        }
    ],
    "parameters": {
        "content_type": "pd"
    }
}

response = requests.post(
    "http://localhost:8080/v2/models/content-type-example/infer",
    json=payload
)
```


```python

```
