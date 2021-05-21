# Content type decoding

MLServer extends the V2 inference protocol by adding support for a `content_type` annotation.
This annotation can be provided either through the model metadata `tags`, or through the input `parameters`.
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

class EchoRuntime(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        outputs = []
        for request_input in payload.inputs:
            decoded_input = self.decode(request_input)
            print(f"------ Encoded Input ({request_input.name}) ------")
            print(json.dumps(request_input.dict(), indent=2))
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
2. Is there any content type defined in the `inputs[].tags.content_type` field within the **model metadata**?
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

## Request Input Parameters

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
            "shape": [11],
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

## Model Metadata

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
            "tags": {
                "content_type": "np"
            }
        },
        {
            "name": "metadata-str",
            "datatype": "BYTES",
            "shape": [11],
            "tags": {
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

## Custom Codecs

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
    ResponseOutput
)
from mlserver.codecs import NumpyCodec, _codec_registry as codecs

class PillowCodec(NumpyCodec):
    ContentType = "img"
    DefaultMode = "L"
    
    def encode(self, name: str, payload: Image) -> ResponseOutput:
        byte_array = io.BytesIO()
        payload.save(byte_array, mode=self.DefaultMode)
        
        return ResponseOutput(
            name=name,
            shape=payload.size,
            datatype="BYTES",
            data=byte_array.getvalue()
        )
    
    def decode(self, request_input: RequestInput) -> Image:
        if request_input.datatype != "BYTES":
            # If not bytes, assume it's an array
            image_array = super().decode(request_input)
            return Image.fromarray(image_array, mode=self.DefaultMode)
        
        encoded = request_input.data.__root__
        if isinstance(encoded, str):
            encoded = encoded.encode()

        return Image.frombytes(
            mode=self.DefaultMode,
            size=request_input.shape,
            data=encoded
        )
    
# Register our new codec so that it's used for payloads with `img` content type
codecs.register(content_type=PillowCodec.ContentType, codec=PillowCodec())

class EchoRuntime(MLModel):
    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        outputs = []
        for request_input in payload.inputs:
            decoded_input = self.decode(request_input)
            print(f"------ Encoded Input ({request_input.name}) ------")
            print(json.dumps(request_input.dict(), indent=2))
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


```python

```
