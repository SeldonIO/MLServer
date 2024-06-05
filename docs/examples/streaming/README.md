# Streaming support

The `mlserver` package comes with built-in support for streaming data. This allows you to process data in real-time, without having to wait for the entire response to be available. It supports both REST and gRPC APIs.

## Overview

In this example, we create a simple `Identity Text Model` which simply splits the input text into words and returns them one by one. We will use this model to demonstrate how to stream the response from the server to the client. This particular example can provide a good starting point for building more complex streaming models such as the ones based on Large Language Models (LLMs) where streaming is an essential feature to hide the latency of the model.

## Serving

The next step will be to serve our model using `mlserver`. For that, we will first implement an extension that serves as the runtime to perform inference using our custom `TextModel`.

### Custom inference runtime

This is a trivial model to demonstrate streaming support. The model simply splits the input text into words and returns them one by one. In this example we do the following:

- split the text into words using the white space as the delimiter.
- wait 0.5 seconds between each word to simulate a slow model.
- return each word one by one.


```python
%%writefile text_model.py

import asyncio
from typing import AsyncIterator
from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import StringCodec


class TextModel(MLModel):

    async def predict_stream(
        self, payloads: AsyncIterator[InferenceRequest]
    ) -> AsyncIterator[InferenceResponse]:
        payload = [_ async for _ in payloads][0]
        text = StringCodec.decode_input(payload.inputs[0])[0]
        words = text.split(" ")

        split_text = []
        for i, word in enumerate(words):
            split_text.append(word if i == 0 else " " + word)

        for word in split_text:
            await asyncio.sleep(0.5)
            yield InferenceResponse(
                model_name=self._settings.name,
                outputs=[
                    StringCodec.encode_output(
                        name="output",
                        payload=[word],
                        use_bytes=True,
                    ),
                ],
            )

```

As it can be seen, the `predict_stream` method receives as an input an `AsyncIterator` of `InferenceRequest` and returns an `AsyncIterator` of `InferenceResponse`. This definition covers all types of possible input-output combinations for streaming: unary-stream, stream-unary, stream-stream. It is up to the client and server to send/receive the appropriate number of requests/responses which should be known apriori.

Note that although unary-unary can be covered by `predict_stream` method as well, `mlserver` already covers that through the `predict` method.

One important limitation to keep in mind is that for the REST API, the client will not be able to send a stream of requests. The client will have to send a single request with the entire input text. The server will then stream the response back to the client. gRPC API, on the other hand, supports all types of streaming listed above.

### Settings file

The next step will be to create 2 configuration files:
- `settings.json`: holds the configuration of our server (e.g. ports, log level, etc.).
- `model-settings.json`: holds the configuration of our model (e.g. input type, runtime to use, etc.).

#### settings.json


```python
%%writefile settings.json

{
  "debug": false,
  "parallel_workers": 0,
  "gzip_enabled": false,
  "metrics_endpoint": null
}

```

Note the currently there are three main limitations of the streaming support in MLServer:

- distributed workers are not supported (i.e., the `parallel_workers` setting should be set to `0`)
- `gzip` middleware is not supported for REST (i.e., `gzip_enabled` setting should be set to `false`)
- metrics endpoint is not available (i.e. `metrics_endpoint` is also disabled for streaming for gRPC)

#### model-settings.json


```python
%%writefile model-settings.json

{
  "name": "text-model",

  "implementation": "text_model.TextModel",
  
  "versions": ["text-model/v1.2.3"],
  "platform": "mlserver",
  "inputs": [
    {
      "datatype": "BYTES",
      "name": "prompt",
      "shape": [1]
    }
  ],
  "outputs": [
    {
      "datatype": "BYTES",
      "name": "output",
      "shape": [1]
    }
  ]
}
```

#### Start serving the model

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be run from the same directory where our config files are or point to the folder where they are.

```bash
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be run in the background on a separate terminal.

#### Inference request

To test our model, we will use the following inference request:


```python
%%writefile generate-request.json

{
    "inputs": [
        {
            "name": "prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": ["What is the capital of France?"],
            "parameters": {
            "content_type": "str"
            }
        }
    ],
    "outputs": [
        {
          "name": "output"
        }
    ]
}
```

### Send test generate stream request (REST)

To send a REST streaming request to the server, we will use the following Python code:


```python
import httpx
from httpx_sse import connect_sse
from mlserver import types
from mlserver.codecs import StringCodec

inference_request = types.InferenceRequest.parse_file("./generate-request.json")

with httpx.Client() as client:
    with connect_sse(client, "POST", "http://localhost:8080/v2/models/text-model/generate_stream", json=inference_request.dict()) as event_source:
        for sse in event_source.iter_sse():
            response = types.InferenceResponse.parse_raw(sse.data)
            print(StringCodec.decode_output(response.outputs[0]))

```

### Send test generate stream request (gRPC)

To send a gRPC streaming request to the server, we will use the following Python code:


```python
import grpc
import mlserver.types as types
from mlserver.codecs import StringCodec
from mlserver.grpc.converters import ModelInferResponseConverter
import mlserver.grpc.converters as converters
import mlserver.grpc.dataplane_pb2_grpc as dataplane

inference_request = types.InferenceRequest.parse_file("./generate-request.json")

# need to convert from string to bytes for grpc
inference_request.inputs[0] = StringCodec.encode_input("prompt", inference_request.inputs[0].data.__root__)
inference_request_g = converters.ModelInferRequestConverter.from_types(
    inference_request, model_name="text-model", model_version=None
)

async def get_inference_request_stream(inference_request):
    yield inference_request

async with grpc.aio.insecure_channel("localhost:8081") as grpc_channel:
    grpc_stub = dataplane.GRPCInferenceServiceStub(grpc_channel)
    inference_request_stream = get_inference_request_stream(inference_request_g)
    
    async for response in grpc_stub.ModelStreamInfer(inference_request_stream):
        response = ModelInferResponseConverter.to_types(response)
        print(StringCodec.decode_output(response.outputs[0]))
```

Note that for gRPC, the request is transformed into an async generator which is then passed to the `ModelStreamInfer` method. The response is also an async generator which can be iterated over to get the response.


