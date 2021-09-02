# Serving Alibi-Detect models

Out of the box, `mlserver` supports the deployment and serving of `alibi-detect` models. In this example, we will cover how we can create a detector configuration to then serve it using `mlserver`.

## Reference Data and Configuration

The first step will be to fetch a reference data for an `alibi-detect` model. For that, we will use the [income Classifier example from the `alibi-detect` documentation](https://docs.seldon.io/projects/alibi-detect/en/latest/examples/cd_chi2ks_adult.html)

Install Alibi dependencies for dataset and detector creation


```python
!pip install alibi alibi_detect
```


```python
import alibi
import matplotlib.pyplot as plt
import numpy as np
```


```python
adult = alibi.datasets.fetch_adult()
X, y = adult.data, adult.target
feature_names = adult.feature_names
category_map = adult.category_map
X.shape, y.shape
```


```python
n_ref = 10000
n_test = 10000

X_ref, X_t0, X_t1 = X[:n_ref], X[n_ref:n_ref + n_test], X[n_ref + n_test:n_ref + 2 * n_test]
X_ref.shape, X_t0.shape, X_t1.shape
```


```python
categories_per_feature = {f: None for f in list(category_map.keys())}
```

### Saving our reference data


```python
detector_data={"x_ref":X_ref,"categories_per_feature":categories_per_feature}
```


```python
import pickle
filepath = 'alibi-detector-artifacts/detector_data.pkl' 
pickle.dump(detector_data, open(filepath,"wb"))
```

## Serving

Now that we have the reference data and other configuration parameters, the next step will be to serve it using `mlserver`. 
For that, we will need to create 2 configuration files: 

- `settings.json`: holds the configuration of our server (e.g. ports, log level, etc.).
- `model-settings.json`: holds the configuration of our model (e.g. input type, runtime to use, etc.).

### `settings.json`


```python
%%writefile settings.json
{
    "debug": "true"
}
```

### `model-settings.json`


```python
%%writefile model-settings.json
{
  "name": "income-classifier-cd",
  "implementation": "mlserver_alibi_detect.AlibiDriftDetectRuntime",
  "parameters": {
    "uri": "./alibi-detector-artifacts/detector_data.pkl",
    "version": "v0.1.0",
    "extra":{
      "detector_type":"alibi_detect.cd.TabularDrift",
      "protocol": "kfserving.http",
      "init_detector": true,
      "init_parameters": {
        "p_val": 0.05
      },
      "predict_parameters": {
        "drift_type": "feature"
      }
    }
  }
}
```

### Start serving our model

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request

We now have our model being served by `mlserver`.
To make sure that everything is working as expected, let's send a request from our test set.

For that, we can use the Python types that `mlserver` provides out of box, or we can build our request manually.

# TabularDrift

### Detecting Drift locally


```python
from alibi_detect.cd import TabularDrift
cd = TabularDrift(X_ref, p_val=.05, categories_per_feature=categories_per_feature)
cd.predict(X_t0,drift_type="feature")
```

### Detecting Drift via MLServer


```python
import requests

inference_request = {
    "inputs": [
        {
            "name": "predict",
            "shape": X_t0.shape,
            "datatype": "FP32",
            "data": X_t0.tolist(),
        }
    ],
}

endpoint = "http://localhost:8080/v2/models/income-classifier-cd/versions/v0.1.0/infer"
response = requests.post(endpoint, json=inference_request)
```


```python
import json
response_dict = json.loads(response.text)
print(response_dict,"\n")

labels = ['No!', 'Yes!']
for f in range(cd.n_features):
    stat = 'Chi2' if f in list(categories_per_feature.keys()) else 'K-S'
    fname = feature_names[f]
    is_drift = response_dict['outputs'][0]['data'][f]
    print(f'{fname} -- Drift? {labels[is_drift]}')
```

### Detecting Drift via custom endpoint for v2 protocol


```python
import requests

inference_request = {
    "inputs": [
        {
            "name": "predict",
            "shape": X_t0.shape,
            "datatype": "FP32",
            "data": X_t0.tolist(),
        }
    ],
}

endpoint = "http://localhost:8080/"
response = requests.post(endpoint, json=inference_request)
```


```python
import json
response_dict = json.loads(response.text)
print(response_dict,"\n")

labels = ['No!', 'Yes!']
for f in range(cd.n_features):
    stat = 'Chi2' if f in list(categories_per_feature.keys()) else 'K-S'
    fname = feature_names[f]
    is_drift = response_dict['data']['is_drift'][f]
    stat_val, p_val = response_dict['data']['distance'][f], response_dict['data']['p_val'][f]
    print(f'{fname} -- Drift? {labels[is_drift]} -- {stat} {stat_val:.3f} -- p-value {p_val:.3f}')
```

### Detecting Drift via custom endpoint for Tensorflow protocol


```python
%%writefile model-settings.json
{
  "name": "income-classifier-cd",
  "implementation": "mlserver_alibi_detect.AlibiDriftDetectRuntime",
  "parameters": {
    "uri": "./alibi-detector-artifacts/detector_data.pkl",
    "version": "v0.1.0",
    "extra":{
      "detector_type":"alibi_detect.cd.TabularDrift",
      "init_detector":true,
      "protocol": "tensorflow.http",
      "init_parameters": {
        "p_val": 0.05
      },
      "predict_parameters": {
        "drift_type": "feature"
      }
    }
  }
}
```

Restart the mlserver after changing the settings file.


```python
import requests

inference_request = {
    "instances": X_t1.tolist()
}

endpoint = "http://localhost:8080/"
response = requests.post(endpoint, json=inference_request)
```


```python
import json
response_dict = json.loads(response.text)
print(response_dict,"\n")

labels = ['No!', 'Yes!']
for f in range(cd.n_features):
    stat = 'Chi2' if f in list(categories_per_feature.keys()) else 'K-S'
    fname = feature_names[f]
    is_drift = response_dict['data']['is_drift'][f]
    stat_val, p_val = response_dict['data']['distance'][f], response_dict['data']['p_val'][f]
    print(f'{fname} -- Drift? {labels[is_drift]} -- {stat} {stat_val:.3f} -- p-value {p_val:.3f}')
```

# ChiSquareDrift

### Detecting Drift locally


```python
cols = list(category_map.keys())
cat_names = [feature_names[_] for _ in list(category_map.keys())]
X_ref_cat, X_t0_cat = X_ref[:, cols], X_t0[:, cols]
X_ref_cat.shape, X_t0_cat.shape
```


```python
from alibi_detect.cd import ChiSquareDrift
cd = ChiSquareDrift(X_ref_cat, p_val=.05)
preds = cd.predict(X_t0_cat,drift_type="feature")
```


```python
labels = ['No!', 'Yes!']
print(f"Threshold {preds['data']['threshold']}")
for f in range(cd.n_features):
    fname = cat_names[f]
    is_drift = (preds['data']['p_val'][f] < preds['data']['threshold']).astype(int)
    stat_val, p_val = preds['data']['distance'][f], preds['data']['p_val'][f]
    print(f'{fname} -- Drift? {labels[is_drift]} -- Chi2 {stat_val:.3f} -- p-value {p_val:.3f}')
```

### Detecting Drift via custom endpoint for Seldon protocol


```python
from alibi_detect.utils.saving import save_detector
filepath = "alibi-detector-artifacts/detector_data_cat"
save_detector(cd, filepath)
```


```python
%%writefile model-settings.json
{
  "name": "income-classifier-cd",
  "implementation": "mlserver_alibi_detect.AlibiDriftDetectRuntime",
  "parameters": {
    "uri": "./alibi-detector-artifacts/detector_data_cat",
    "version": "v0.1.0",
    "extra":{
      "detector_type":"alibi_detect.cd.ChiSquareDrift",
      "init_detector": false,
      "protocol": "seldon.http",
      "predict_parameters": {
        "drift_type": "feature"
      }
    }
  }
}
```

Restart the mlserver after changing the settings file.


```python
import requests

inference_request = {
    "data":{
        "ndarray": X_t0_cat.tolist()
    }
}

endpoint = "http://localhost:8080/"
response = requests.post(endpoint, json=inference_request)
```


```python
import json
response_dict = json.loads(response.text)
print(response_dict,"\n")

labels = ['No!', 'Yes!']
for f in range(cd.n_features):
    stat = 'Chi2' if f in list(categories_per_feature.keys()) else 'K-S'
    fname = cat_names[f]
    is_drift = response_dict['data']['is_drift'][f]
    stat_val, p_val = response_dict['data']['distance'][f], response_dict['data']['p_val'][f]
    print(f'{fname} -- Drift? {labels[is_drift]} -- {stat} {stat_val:.3f} -- p-value {p_val:.3f}')
```
