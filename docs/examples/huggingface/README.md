# Serving HuggingFace Transformer Models

Out of the box, MLServer supports the deployment and serving of HuggingFace Transformer models with the following features:

- Loading of Transformer Model artifacts from the Hugging Face Hub.
- Model quantization & optimization using the Hugging Face Optimum library
- Request batching for GPU optimization (via adaptive batching and request batching)

In this example, we will showcase some of this features using an example model.


```python
# Import required dependencies
import requests
```

## Serving

Now that we have trained and serialised our model, we are ready to start serving it.
For that, the initial step will be to set up a `model-settings.json` that instructs MLServer to load our artifact using the HuggingFace Inference Runtime.

We will show how to add share a task 


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parameters": {
        "extra": {
            "task": "text-generation",
            "pretrained_model": "distilgpt2"
        }
    }
}
```

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request



```python
inference_request = {
    "inputs": [
        {
          "name": "args",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["this is a test"],
        }
    ]
}

requests.post("http://localhost:8080/v2/models/transformer/infer", json=inference_request).json()
```

### Using Optimum Optimized Models

We can also leverage the Optimum library that allows us to access quantized and optimized models. 

We can download pretrained optimized models from the hub if available by enabling the `optimum_model` flag:


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parameters": {
        "extra": {
            "task": "text-generation",
            "pretrained_model": "distilgpt2",
            "optimum_model": true
        }
    }
}
```

Once again, you are able to run the model using the MLServer CLI. As before this needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

### Send Test Request to Optimum Optimized Model

The request can now be sent using the same request structure but using optimized models for better performance.


```python
inference_request = {
    "inputs": [
        {
          "name": "args",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["this is a test"],
        }
    ]
}

requests.post("http://localhost:8080/v2/models/transformer/infer", json=inference_request).json()
```

## Testing Supported Tasks

We can support multiple other transformers other than just text generation, below includes examples for a few other tasks supported.



### Question Answering


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parameters": {
        "extra": {
            "task": "question-answering"
        }
    }
}
```

Once again, you are able to run the model using the MLServer CLI.

```shell
mlserver start .
```


```python
inference_request = {
    "inputs": [
        {
          "name": "question",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["what is your name?"],
        },
        {
          "name": "context",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["Hello, I am Seldon, how is it going"],
        }
    ]
}

requests.post("http://localhost:8080/v2/models/transformer/infer", json=inference_request).json()
```

### Sentiment Analysis


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parameters": {
        "extra": {
            "task": "text-classification"
        }
    }
}
```

Once again, you are able to run the model using the MLServer CLI.

```shell
mlserver start .
```


```python
inference_request = {
    "inputs": [
        {
          "name": "args",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["This is terrible!"],
        }
    ]
}

requests.post("http://localhost:8080/v2/models/transformer/infer", json=inference_request).json()
```

## GPU Acceleration

We can also evaluate GPU acceleration, we can test the speed on CPU vs GPU using the following parameters

### Testing with CPU

We first test the time taken with the device=-1 which configures CPU by default


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "max_batch_size": 128,
    "max_batch_time": 1,
    "parameters": {
        "extra": {
            "task": "text-generation",
            "device": -1
        }
    }
}
```

Once again, you are able to run the model using the MLServer CLI.

```shell
mlserver start .
```


```python
inference_request = {
    "inputs": [
        {
          "name": "text_inputs",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["This is a generation for the work" for i in range(512)],
        }
    ]
}

# Benchmark time
import time
start_time = time.monotonic()

requests.post("http://localhost:8080/v2/models/transformer/infer", json=inference_request)

print(f"Elapsed time: {time.monotonic() - start_time}")
```

We can see that it takes 81 seconds which is 8 times longer than the gpu example below.

### Testing with GPU

IMPORTANT: Running the code below requries having a machine with GPU configured correctly to work for Tensorflow/Pytorch.
    
Now we'll run the benchmark with GPU configured, which we can do by setting `device=0`


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parameters": {
        "extra": {
            "task": "text-generation",
            "device": 0
        }
    }
}
```


```python
inference_request = {
    "inputs": [
        {
          "name": "text_inputs",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["This is a generation for the work" for i in range(512)],
        }
    ]
}

# Benchmark time
import time
start_time = time.monotonic()

requests.post("http://localhost:8080/v2/models/transformer/infer", json=inference_request)

print(f"Elapsed time: {time.monotonic() - start_time}")
```

We can see that the elapsed time is 8 times less than the CPU version!

### Adaptive Batching with GPU

We can also see how the adaptive batching capabilities can allow for GPU acceleration by grouping multiple incoming requests so they get processed in GPU batch.

In our case we can enable adaptive batching with the `max_batch_size` which in our case we will set it ot 128.

We will also configure `max_batch_time` which specifies` the maximum amount of time the MLServer orchestrator will wait before sending for inference.


```python
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "max_batch_size": 128,
    "max_batch_time": 1,
    "parameters": {
        "extra": {
            "task": "text-generation",
            "pretrained_model": "distilgpt2",
            "device": 0
        }
    }
}
```

In order to achieve the throughput required of 50 requests per second, we will use the tool `vegeta` which performs load testing.

We can now see that we are able to see that the requests are batched and we receive 100% success eventhough the requests are sent one-by-one.


```bash
%%bash
jq -ncM '{"method": "POST", "header": {"Content-Type": ["application/json"] }, "url": "http://localhost:8080/v2/models/transformer/infer", "body": "{\"inputs\":[{\"name\":\"text_inputs\",\"shape\":[1],\"datatype\":\"BYTES\",\"data\":[\"test\"]}]}" | @base64 }' \
          | vegeta \
                -cpus="2" \
                attack \
                -duration="3s" \
                -rate="50" \
                -format=json \
          | vegeta \
                report \
                -type=text
```


```python

```
