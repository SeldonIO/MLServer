# Serving Alibi-Detect models

Out of the box, `mlserver` supports the deployment and serving of [alibi_detect](https://docs.seldon.io/projects/alibi-detect/en/latest/index.html) models. Alibi Detect is an open source Python library focused on outlier, adversarial and drift detection. In this example, we will cover how we can create a detector configuration to then serve it using `mlserver`.

## Fetch reference data

The first step will be to fetch a reference data and other relevant metadata for an `alibi-detect` model.

For that, we will use the [alibi](https://github.com/SeldonIO/alibi) library to get the adult dataset with [demographic features from a 1996 US census](https://archive.ics.uci.edu/ml/datasets/census+income).

````{note}
Install `alibi` library for dataset dependencies and `alibi_detect` library for detector configuration from Pypi
```python
!pip install alibi alibi_detect
```
````

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
```

```python
n_ref = 10000
n_test = 10000

X_ref, X_t0, X_t1 = X[:n_ref], X[n_ref:n_ref + n_test], X[n_ref + n_test:n_ref + 2 * n_test]
categories_per_feature = {f: None for f in list(category_map.keys())}
```

## Drift Detector Configuration

This example is based on the Categorical and mixed type data drift detection on income prediction tabular data from the [alibi-detect](https://docs.seldon.io/projects/alibi-detect/en/latest/examples/cd_chi2ks_adult.html) documentation.

### Creating detector and saving configuration

```python
from alibi_detect.cd import TabularDrift
cd_tabular = TabularDrift(X_ref, p_val=.05, categories_per_feature=categories_per_feature)
```

```python
from alibi_detect.utils.saving import save_detector
filepath = "alibi-detector-artifacts"
save_detector(cd_tabular, filepath)
```

### Detecting data drift directly

```python
preds = cd_tabular.predict(X_t0,drift_type="feature")

labels = ['No!', 'Yes!']
print(f"Threshold {preds['data']['threshold']}")
for f in range(cd_tabular.n_features):
    fname = feature_names[f]
    is_drift = (preds['data']['p_val'][f] < preds['data']['threshold']).astype(int)
    stat_val, p_val = preds['data']['distance'][f], preds['data']['p_val'][f]
    print(f'{fname} -- Drift? {labels[is_drift]} -- Chi2 {stat_val:.3f} -- p-value {p_val:.3f}')
```

    Threshold 0.05
    Age -- Drift? No! -- Chi2 0.012 -- p-value 0.508
    Workclass -- Drift? No! -- Chi2 8.487 -- p-value 0.387
    Education -- Drift? No! -- Chi2 4.753 -- p-value 0.576
    Marital Status -- Drift? No! -- Chi2 3.160 -- p-value 0.368
    Occupation -- Drift? No! -- Chi2 8.194 -- p-value 0.415
    Relationship -- Drift? No! -- Chi2 0.485 -- p-value 0.993
    Race -- Drift? No! -- Chi2 0.587 -- p-value 0.965
    Sex -- Drift? No! -- Chi2 0.217 -- p-value 0.641
    Capital Gain -- Drift? No! -- Chi2 0.002 -- p-value 1.000
    Capital Loss -- Drift? No! -- Chi2 0.002 -- p-value 1.000
    Hours per week -- Drift? No! -- Chi2 0.012 -- p-value 0.508
    Country -- Drift? No! -- Chi2 9.991 -- p-value 0.441

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

    Overwriting settings.json

### `model-settings.json`

```python
%%writefile model-settings.json
{
  "name": "income-tabular-drift",
  "implementation": "mlserver_alibi_detect.AlibiDetectRuntime",
  "parameters": {
    "uri": "./alibi-detector-artifacts",
    "version": "v0.1.0",
    "extra": {
      "predict_parameters":{
        "drift_type": "feature"
      }
    }
  }
}
```

    Overwriting model-settings.json

### Start serving our model

Now that we have our config in-place, we can start the server by running mlserver start command. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request

We now have our alibi-detect model being served by `mlserver`. To make sure that everything is working as expected, let's send a request from our test set.

For that, we can use the Python types that `mlserver` provides out of box, or we can build our request manually.

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
    ]
}

endpoint = "http://localhost:8080/v2/models/income-tabular-drift/versions/v0.1.0/infer"
response = requests.post(endpoint, json=inference_request)
```

### View model response

```python
import json
response_dict = json.loads(response.text)

labels = ['No!', 'Yes!']
for f in range(cd_tabular.n_features):
    stat = 'Chi2' if f in list(categories_per_feature.keys()) else 'K-S'
    fname = feature_names[f]
    is_drift = response_dict['outputs'][0]['data'][f]
    stat_val, p_val = response_dict['outputs'][1]['data'][f], response_dict['outputs'][2]['data'][f]
    print(f'{fname} -- Drift? {labels[is_drift]} -- Chi2 {stat_val:.3f} -- p-value {p_val:.3f}')
```

    Age -- Drift? No! -- Chi2 0.012 -- p-value 0.508
    Workclass -- Drift? No! -- Chi2 8.487 -- p-value 0.387
    Education -- Drift? No! -- Chi2 4.753 -- p-value 0.576
    Marital Status -- Drift? No! -- Chi2 3.160 -- p-value 0.368
    Occupation -- Drift? No! -- Chi2 8.194 -- p-value 0.415
    Relationship -- Drift? No! -- Chi2 0.485 -- p-value 0.993
    Race -- Drift? No! -- Chi2 0.587 -- p-value 0.965
    Sex -- Drift? No! -- Chi2 0.217 -- p-value 0.641
    Capital Gain -- Drift? No! -- Chi2 0.002 -- p-value 1.000
    Capital Loss -- Drift? No! -- Chi2 0.002 -- p-value 1.000
    Hours per week -- Drift? No! -- Chi2 0.012 -- p-value 0.508
    Country -- Drift? No! -- Chi2 9.991 -- p-value 0.441
