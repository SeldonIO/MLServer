# Serving HuggingFace Transformer Models

Out of the box, MLServer supports the deployment and serving of HuggingFace Transformer models with the following features:

- Loading of Transformer Model artifacts from Hub.
- Supports Optimized models using Optimum library

In this example, we will showcase some of this features using an example model.


```
# Import required dependencies
import requests
```

## Serving

Now that we have trained and serialised our model, we are ready to start serving it.
For that, the initial step will be to set up a `model-settings.json` that instructs MLServer to load our artifact using the HuggingFace Inference Runtime.


```
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parallel_workers": 0,
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



```
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




    {'model_name': 'transformer',
     'model_version': None,
     'id': '9b24304e-730f-4a98-bfde-8949851388a9',
     'parameters': None,
     'outputs': [{'name': 'output',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['[{"generated_text": "this is a test-case where you\'re checking if someone\'s going to have an encrypted file that they like to open, or whether their file has a hidden contents if their file is not opened. If it\'s the same file, when all the"}]']}]}



### Using Optimum Optimized Models

We can also leverage the Optimum library that allows us to access quantized and optimized models. 

We can download pretrained optimized models from the hub if available by enabling the `optimum_model` flag:


```
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parallel_workers": 0,
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


```
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




    {'model_name': 'transformer',
     'model_version': None,
     'id': '296ea44e-7696-4584-af5a-148a7083b2e7',
     'parameters': None,
     'outputs': [{'name': 'output',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['[{"generated_text": "this is a test that allows us to define the value type, and a function is defined directly with these variables.\\n\\n\\nThe function is defined for a parameter with type\\nIn this example,\\nif you pass a message function like\\ntype"}]']}]}



## Testing Supported Tasks

We can support multiple other transformers other than just text generation, below includes examples for a few other tasks supported.



### Question Answering


```
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parallel_workers": 0,
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


```
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




    {'model_name': 'gpt2-model',
     'model_version': None,
     'id': '204ad4e7-79ea-40b4-8efb-aed16dedf7ed',
     'parameters': None,
     'outputs': [{'name': 'output',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['{"score": 0.9869922995567322, "start": 12, "end": 18, "answer": "Seldon"}']}]}



### Sentiment Analysis


```
%%writefile ./model-settings.json
{
    "name": "transformer",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parallel_workers": 0,
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


```
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




    {'model_name': 'transformer',
     'model_version': None,
     'id': '463ceddb-f426-4815-9c46-9fa9fc5272b1',
     'parameters': None,
     'outputs': [{'name': 'output',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['[{"label": "NEGATIVE", "score": 0.9996137022972107}]']}]}




```

```
