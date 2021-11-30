# Serving a custom model with JSON serialization

The `mlserver` package comes with inference runtime implementations for `scikit-learn` and `xgboost` models.
However, some times we may also need to roll out our own inference server, with custom logic to perform inference.
To support this scenario, MLServer makes it really easy to create your own extensions, which can then be containerised and deployed in a production environment.

## Overview

In this example, we create a simple `Hello World JSON` model that parses and modifies a JSON data chunk. This is often useful as a means to
quickly bootstrap existing models that utilize JSON based model inputs.

## Serving

The next step will be to serve our model using `mlserver`. 
For that, we will first implement an extension which serve as the _runtime_ to perform inference using our custom `Hello World JSON` model.

### Custom inference runtime

This is a trivial model to demonstrate how to conceptially work with JSON inputs / outputs. In this example:

- Parse the JSON input from the client
- Create a JSON response echoing back the client request as well as a server generated message



```python
%%writefile models.py
import json

from typing import Dict, Any
from mlserver import MLModel, types
from mlserver.codecs import StringCodec

from mlserver.cli.main import main


class JsonHelloWorldModel(MLModel):
    async def load(self) -> bool:
        # Perform additional custom initialization here.
        print("Initialize model")

        # Set readiness flag for model
        return await super().load()
    
    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        request = self._extract_json(payload)
        response = { 
            "request": request,
            "server_response": f"Got your request. Hello from the server."
        }
        response_bytes = json.dumps(response).encode("UTF-8")

        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name="echo_response",
                    shape=[len(response_bytes)],
                    datatype="BYTES",
                    data=[response_bytes],
                    parameters=types.Parameters(content_type="str")
                )
            ]
        )

    def _extract_json(self, payload: types.InferenceRequest) -> Dict[str, Any]:
        inputs = {}
        for inp in payload.inputs:
            inputs[inp.name] = json.loads("".join(self.decode(inp)))

        return inputs

```

### Settings files

The next step will be to create 2 configuration files: 

- `settings.json`: holds the configuration of our server (e.g. ports, log level, etc.).
- `model-settings.json`: holds the configuration of our model (e.g. input type, runtime to use, etc.).

#### `settings.json`


```python
%%writefile settings.json
{
    "debug": "true"
}
```

#### `model-settings.json`


```python
%%writefile model-settings.json
{
    "name": "json-hello-world",
    "implementation": "models.JsonHelloWorldModel"
}
```

### Start serving our model

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request (REST)


We now have our model being served by `mlserver`.
To make sure that everything is working as expected, let's send a request from our test set.

For that, we can use the Python types that `mlserver` provides out of box, or we can build our request manually.


```python
import requests
import json

inputs = {
    "name": "Foo Bar",
    "message": "Hello from Client (REST)!"
}

# NOTE: this uses characters rather than encoded bytes. It is recommended that you use the `mlserver` types to assist in the correct encoding.
inputs_string= json.dumps(inputs)

inference_request = {
    "inputs": [
        {
            "name": "echo_request",
            "shape": [len(inputs_string)],
            "datatype": "BYTES",
            "data": [inputs_string]
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/json-hello-world/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```

### Send test inference request (gRPC)


Utilizing string data with the gRPC interface can be a bit tricky. To ensure we are correctly handling inputs and
outputs we will be handled correctly.

For simplicity in this case, we leverage the Python types that `mlserver` provides out of the box. Alternatively,
the gRPC stubs can be generated regenerated from the V2 specification directly for use by non-Python as well as 
Python clients.


```python
import requests
import json
import grpc
import mlserver.grpc.converters as converters
import mlserver.grpc.dataplane_pb2_grpc as dataplane
import mlserver.types as types

model_name = "json-hello-world"
inputs = {
    "name": "Foo Bar",
    "message": "Hello from Client (gRPC)!"
}
inputs_bytes = json.dumps(inputs).encode("UTF-8")

inference_request = types.InferenceRequest(
    inputs=[
        types.RequestInput(
            name="echo_request",
            shape=[len(inputs_bytes)],
            datatype="BYTES",
            data=[inputs_bytes],
            parameters=types.Parameters(content_type="str")
        )
    ]
)

inference_request_g = converters.ModelInferRequestConverter.from_types(
    inference_request,
    model_name=model_name,
    model_version=None
)

grpc_channel = grpc.insecure_channel("localhost:8081")
grpc_stub = dataplane.GRPCInferenceServiceStub(grpc_channel)

response = grpc_stub.ModelInfer(inference_request_g)
response
```

## Deployment

Now that we have written and tested our custom model, the next step is to deploy it.
With that goal in mind, the rough outline of steps will be to first build a custom image containing our code, and then deploy it.


### Building a custom image

```{note}
This section expects that Docker is available and running in the background. 
```

MLServer offers helpers to build a custom Docker image containing your code.
In this example, we will use the `mlserver build` subcommand to create an image, which we'll be able to deploy later.


Note that this section expects that Docker is available and running in the background, as well as a functional cluster with Seldon Core installed and some familiarity with `kubectl`. 


```bash
%%bash
mlserver build . -t 'my-custom-json-server'
```

To ensure that the image is fully functional, we can spin up a container and then send a test request. To start the container, you can run something along the following lines in a separate terminal:

```bash
docker run -it --rm -p 8080:8080 -p 8081:8081 my-custom-json-server
```


```python
import requests
import json
import mlserver.types as types

inputs = {
    "name": "Foo Bar",
    "message": "Hello from Client (REST - Docker)!"
}

inputs_bytes = json.dumps(inputs).encode("UTF-8")

inference_request = types.InferenceRequest(
    inputs=[
        types.RequestInput(
            name="echo_request",
            shape=[len(inputs_bytes)],
            datatype="BYTES",
            data=[inputs_bytes],
            parameters=types.Parameters(content_type="str")
        )
    ]
)

endpoint = "http://localhost:8080/v2/models/json-hello-world/infer"
response = requests.post(endpoint, json=json.loads(inference_request.json(include={"inputs"})))

response.json()
```

As we should be able to see, the server running within our Docker image responds as expected.

### Deploying our custom image

```{note}
This section expects access to a functional Kubernetes cluster with Seldon Core installed and some familiarity with `kubectl`. 
```

Now that we've built a custom image and verified that it works as expected, we can move to the next step and deploy it.
There is a large number of tools out there to deploy images.
However, for our example, we will focus on deploying it to a cluster running [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/).

For that, we will need to create a `SeldonDeployment` resource which instructs Seldon Core to deploy a model embedded within our custom image and compliant with the [V2 Inference Protocol](https://github.com/kserve/kserve/tree/master/docs/predict-api/v2).
This can be achieved by _applying_ (i.e. `kubectl apply`) a `SeldonDeployment` manifest to the cluster, similar to the one below:


```python
%%writefile seldondeployment.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: json-hello-world
spec:
  predictors:
    - name: default
      annotations:
        seldon.io/no-engine: "true"
      graph:
        name: json-server
        type: MODEL
      componentSpecs:
        - spec:
            containers:
              - name: json-server
                image: my-custom-json-server
                ports:
                  - containerPort: 8080
                    name: http
                    protocol: TCP
                  - containerPort: 8081
                    name: grpc
                    protocol: TCP
```
