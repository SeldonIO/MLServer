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

Since we're using a pretrained model, we can skip straight to serving.

### `model-settings.json`


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

    Overwriting ./model-settings.json


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

requests.post(
    "http://localhost:8080/v2/models/transformer/infer", json=inference_request
).json()
```




    {'model_name': 'transformer',
     'id': 'eb160c6b-8223-4342-ad92-6ac301a9fa5d',
     'parameters': {},
     'outputs': [{'name': 'output',
       'shape': [1, 1],
       'datatype': 'BYTES',
       'parameters': {'content_type': 'hg_jsonlist'},
       'data': ['{"generated_text": "this is a testnet with 1-3,000-bit nodes as nodes."}']}]}



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

    Overwriting ./model-settings.json


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

requests.post(
    "http://localhost:8080/v2/models/transformer/infer", json=inference_request
).json()
```




    {'model_name': 'transformer',
     'id': '9c482c8d-b21e-44b1-8a42-7650a9dc01ef',
     'parameters': {},
     'outputs': [{'name': 'output',
       'shape': [1, 1],
       'datatype': 'BYTES',
       'parameters': {'content_type': 'hg_jsonlist'},
       'data': ['{"generated_text": "this is a test of the \\"safe-code-safe-code-safe-code\\" approach. The method only accepts two parameters as parameters: the code. The parameter \'unsafe-code-safe-code-safe-code\' should"}']}]}



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

    Overwriting ./model-settings.json


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
        },
    ]
}

requests.post(
    "http://localhost:8080/v2/models/transformer/infer", json=inference_request
).json()
```




    {'model_name': 'transformer',
     'id': '4efac938-86d8-41a1-b78f-7690b2dcf197',
     'parameters': {},
     'outputs': [{'name': 'output',
       'shape': [1, 1],
       'datatype': 'BYTES',
       'parameters': {'content_type': 'hg_jsonlist'},
       'data': ['{"score": 0.9869915843009949, "start": 12, "end": 18, "answer": "Seldon"}']}]}



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

    Overwriting ./model-settings.json


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

requests.post(
    "http://localhost:8080/v2/models/transformer/infer", json=inference_request
).json()
```




    {'model_name': 'transformer',
     'id': '835eabbd-daeb-4423-a64f-a7c4d7c60a9b',
     'parameters': {},
     'outputs': [{'name': 'output',
       'shape': [1, 1],
       'datatype': 'BYTES',
       'parameters': {'content_type': 'hg_jsonlist'},
       'data': ['{"label": "NEGATIVE", "score": 0.9996137022972107}']}]}



### Masked Language Modeling

We can also serve a masked language model. In the following example, we also build the `huggingface` runtime with the `-E japanese` flag to enable support for Japanese tokenizers.

```python
%%writefile ./model-settings.json
{
  "name": "model",
  "implementation": "mlserver_huggingface.runtime.HuggingFaceRuntime",
  "parameters": {
    "extra": {
      "task": "fill-mask",
      "pretrained_model": "cl-tohoku/bert-base-japanese",
      "pretrained_tokenizer": "cl-tohoku/bert-base-japanese"
    }
  }
}
```
Using the shell to start mlserver like so,
```shell
mlserver start .
```
we can pass inferences like this. Note the `[MASK]` token. The mask token can be different for different models, so check the HuggingFace model config for special tokens.
```python
# Test sentence: Is the sky really [MASK]?
test_sentence = "実際に空が[MASK]のか？"
# [MASK] = visible
expected_output = "見える"
inference_request = {
    "inputs": [
        test_sentence
    ]
}
```
```
Response:
{'model_name': 'transformer', 'id': '9e966d8d-b43d-4ab4-8d47-90e367196233', 'parameters': {}, 'outputs': [{'name': 'output', 'shape': [5, 1], 'datatype': 'BYTES', 'parameters': {'content_type': 'hg_jsonlist'}, 'data': ['{"score": 0.3277095854282379, "token": 11819, "token_str": "\\u3042\\u308b", "sequence": "\\u5b9f\\u969b \\u306b \\u7a7a \\u304c \\u3042\\u308b \\u306e \\u304b?"}', '{"score": 0.10271108895540237, "token": 14656, "token_str": "\\u898b\\u3048\\u308b", "sequence": "\\u5b9f\\u969b \\u306b \\u7a7a \\u304c \\u898b\\u3048\\u308b \\u306e \\u304b?"}', '{"score": 0.08325661718845367, "token": 11835, "token_str": "\\u306a\\u3044", "sequence": "\\u5b9f\\u969b \\u306b \\u7a7a \\u304c \\u306a\\u3044 \\u306e \\u304b?"}', '{"score": 0.036131054162979126, "token": 18413, "token_str": "\\u6b63\\u3057\\u3044", "sequence": "\\u5b9f\\u969b \\u306b \\u7a7a \\u304c \\u6b63\\u3057\\u3044 \\u306e \\u304b?"}', '{"score": 0.029351236298680305, "token": 11820, "token_str": "\\u3044\\u308b", "sequence": "\\u5b9f\\u969b \\u306b \\u7a7a \\u304c \\u3044\\u308b \\u306e \\u304b?"}']}]}
Data:
{'score': 0.3277095854282379, 'token': 11819, 'token_str': 'ある', 'sequence': '実際 に 空 が ある の か?'}
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

    Overwriting ./model-settings.json


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

requests.post(
    "http://localhost:8080/v2/models/transformer/infer", json=inference_request
)

print(f"Elapsed time: {time.monotonic() - start_time}")
```

    Elapsed time: 66.42268538899953


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

    Overwriting ./model-settings.json



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

requests.post(
    "http://localhost:8080/v2/models/transformer/infer", json=inference_request
)

print(f"Elapsed time: {time.monotonic() - start_time}")
```

    Elapsed time: 11.27933280000434


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

    Overwriting ./model-settings.json


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

    Requests      [total, rate, throughput]         150, 50.34, 22.28
    Duration      [total, attack, wait]             6.732s, 2.98s, 3.753s
    Latencies     [min, mean, 50, 90, 95, 99, max]  1.975s, 3.168s, 3.22s, 4.065s, 4.183s, 4.299s, 4.318s
    Bytes In      [total, mean]                     60978, 406.52
    Bytes Out     [total, mean]                     12300, 82.00
    Success       [ratio]                           100.00%
    Status Codes  [code:count]                      200:150  
    Error Set:



```python

```
