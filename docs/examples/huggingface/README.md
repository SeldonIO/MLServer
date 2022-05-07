# Serving HuggingFace Transformer Models

Out of the box, MLServer supports the deployment and serving of HuggingFace Transformer models with the following features:

- Loading of Transformer Model artifacts from Hub.
- Supports Optimized models using Optimum library

In this example, we will showcase some of this features using an example model.


```python
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))
```

## Serving

Now that we have trained and serialised our model, we are ready to start serving it.
For that, the initial step will be to set up a `model-settings.json` that instructs MLServer to load our artifact using the HuggingFace Inference Runtime.


```python
%%writetemplate ./model-settings.json
{{
    "name": "gpt2-model",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parallel_workers": 0,
    "parameters": {{
        "extra": {{
            "task": "text-generation",
            "pretrained_model": "distilgpt2"
        }}
    }}
}}
```

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request



```python
import requests

inference_request = {
    "inputs": [
        {
          "name": "huggingface",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["this is a test"],
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/gpt2-model/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```




    {'model_name': 'gpt2-model',
     'model_version': None,
     'id': 'f65f1b35-840e-4872-83b8-270271501b6c',
     'parameters': None,
     'outputs': [{'name': 'huggingface',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['[[{"generated_text": "this is a test of this. Once it is finished, it will generate a clean and easy clean install page and the build file will be loaded in the terminal. I need to install the build files for this project.\\n\\nNow to have my"}]]']}]}



### Using Optimum Optimized Models

We can also leverage the Optimum library that allows us to access quantized and optimized models. 

We can download pretrained optimized models from the hub if available by enabling the `optimum_model` flag:


```python
%%writetemplate ./model-settings.json
{{
    "name": "gpt2-model",
    "implementation": "mlserver_huggingface.HuggingFaceRuntime",
    "parallel_workers": 0,
    "parameters": {{
        "extra": {{
            "task": "text-generation",
            "pretrained_model": "distilgpt2",
            "optimum_model": true
        }}
    }}
}}
```

Once again, you are able to run the model using the MLServer CLI. As before this needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

### Send Test Request to Optimum Optimized Model


```python
import requests

inference_request = {
    "inputs": [
        {
          "name": "huggingface",
          "shape": [1],
          "datatype": "BYTES",
          "data": ["this is a test"],
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/gpt2-model/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```




    {'model_name': 'gpt2-model',
     'model_version': None,
     'id': 'fdce1497-6b14-4fc6-a414-d437ca7783c6',
     'parameters': None,
     'outputs': [{'name': 'huggingface',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['[[{"generated_text": "this is a test case where I get a message telling me not to let the system know.\\nThis post was created using the \\"Help Coding Standard\\" tool. You can find information about the standard version of the Coding Standard here."}]]']}]}




```python

```
