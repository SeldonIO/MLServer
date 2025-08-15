# Multi-Model Serving

MLServer has been built with [Multi-Model Serving (MMS)](https://www.seldon.io/what-is-multi-model-serving-and-how-does-it-transform-your-ml-infrastructure) in mind.
This means that, within a single instance of MLServer, you can serve multiple models under different paths.
This also includes multiple versions of the same model.

This notebook shows an example of how you can leverage MMS with MLServer.

## Training

We will first start by training 2 different models:

| Name               | Framework      | Source                                                                                                                                              | Trained Model Path          |
| ------------------ | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `mnist-svm`        | `scikit-learn` | [MNIST example from the `scikit-learn` documentation](https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html) | `./models/mnist-svm/model.joblib`        |
| `mushroom-xgboost` | `xgboost`      | [Mushrooms example from the `xgboost` Getting Started guide](https://xgboost.readthedocs.io/en/latest/get_started.html#python)                      | `./models/mushroom-xgboost/model.json` |


### Training our `mnist-svm` model


```python
# Original source code and more details can be found in:
# https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html

# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split

# The digits dataset
digits = datasets.load_digits()

# To apply a classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.001)

# Split data into train and test subsets
X_train, X_test_digits, y_train, y_test_digits = train_test_split(
    data, digits.target, test_size=0.5, shuffle=False)

# We learn the digits on the first half of the digits
classifier.fit(X_train, y_train)
```


```python
import joblib
import os

mnist_svm_path = os.path.join("models", "mnist-svm")
os.makedirs(mnist_svm_path, exist_ok=True)

mnist_svm_model_path = os.path.join(mnist_svm_path, "model.joblib")
joblib.dump(classifier, mnist_svm_model_path)
```

### Training our `mushroom-xgboost` model


```python
# Original code and extra details can be found in:
# https://xgboost.readthedocs.io/en/latest/get_started.html#python

import os
import xgboost as xgb
import requests

from urllib.parse import urlparse
from sklearn.datasets import load_svmlight_file


TRAIN_DATASET_URL = 'https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train'
TEST_DATASET_URL = 'https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test'


def _download_file(url: str) -> str:
    parsed = urlparse(url)
    file_name = os.path.basename(parsed.path)
    file_path = os.path.join(os.getcwd(), file_name)
    
    res = requests.get(url)
    
    with open(file_path, 'wb') as file:
        file.write(res.content)
    
    return file_path

train_dataset_path = _download_file(TRAIN_DATASET_URL)
test_dataset_path = _download_file(TEST_DATASET_URL)

# NOTE: Workaround to load SVMLight files from the XGBoost example
X_train, y_train = load_svmlight_file(train_dataset_path)
X_test_agar, y_test_agar = load_svmlight_file(test_dataset_path)
X_train = X_train.toarray()
X_test_agar = X_test_agar.toarray()

# read in data
dtrain = xgb.DMatrix(data=X_train, label=y_train)

# specify parameters via map
param = {'max_depth':2, 'eta':1, 'objective':'binary:logistic' }
num_round = 2
bst = xgb.train(param, dtrain, num_round)

bst
```


```python
import os

mushroom_xgboost_path = os.path.join("models", "mushroom-xgboost")
os.makedirs(mushroom_xgboost_path, exist_ok=True)

mushroom_xgboost_model_path = os.path.join(mushroom_xgboost_path, "model.json")
bst.save_model(mushroom_xgboost_model_path)
```

## Serving

The next step will be serving both our models within the same MLServer instance.
For that, we will just need to create a `model-settings.json` file local to each of our models and a server-wide `settings.json`.
That is,

- `settings.json`: holds the configuration of our server (e.g. ports, log level, etc.).
- `models/mnist-svm/model-settings.json`: holds the configuration specific to our `mnist-svm` model (e.g. input type, runtime to use, etc.).
- `models/mushroom-xgboost/model-settings.json`: holds the configuration specific to our `mushroom-xgboost` model (e.g. input type, runtime to use, etc.).



### `settings.json`


```python
%%writefile settings.json
{
    "debug": "true"
}
```

### `models/mnist-svm/model-settings.json`


```python
%%writefile models/mnist-svm/model-settings.json
{
    "name": "mnist-svm",
    "implementation": "mlserver_sklearn.SKLearnModel",
    "parameters": {
        "version": "v0.1.0"
    }
}
```

### `models/mushroom-xgboost/model-settings.json`


```python
%%writefile models/mushroom-xgboost/model-settings.json
{
    "name": "mushroom-xgboost",
    "implementation": "mlserver_xgboost.XGBoostModel",
    "parameters": {
        "version": "v0.1.0"
    }
}

```

### Start serving our model

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

## Testing

By this point, we should have both our models getting served by MLServer.
To make sure that everything is working as expected, let's send a request from each test set.

For that, we can use the Python types that the `mlserver` package provides out of box, or we can build our request manually.

### Testing our `mnist-svm` model


```python
import requests

x_0 = X_test_digits[0:1]
inference_request = {
    "inputs": [
        {
          "name": "predict",
          "shape": x_0.shape,
          "datatype": "FP32",
          "data": x_0.tolist()
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/mnist-svm/versions/v0.1.0/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```

### Testing our `mushroom-xgboost` model


```python
import requests

x_0 = X_test_agar[0:1]
inference_request = {
    "inputs": [
        {
          "name": "predict",
          "shape": x_0.shape,
          "datatype": "FP32",
          "data": x_0.tolist()
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/mushroom-xgboost/versions/v0.1.0/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```


```python

```
