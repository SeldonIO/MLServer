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
    "parameters": {{
        "extra": {{
            "task": "text-generation"
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
          "data": ["this is an input"],
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/gpt2-model/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```




    {'model_name': 'gpt2-model',
     'model_version': None,
     'id': 'e07b488b-7730-4a52-a7a0-76bfeaeeffea',
     'parameters': None,
     'outputs': [{'name': 'huggingface',
       'shape': [1],
       'datatype': 'BYTES',
       'parameters': None,
       'data': ['[[{"generated_text": "this is an input device (i.e. a USB), it will be able to interpret messages sent to the USB through the Bluetooth protocol.\\n\\nWhen the input device is plugged in it will ask for data from your iPhone using the NFC,"}]]']}]}




```python

```
