# Serving LightGBM models

Out of the box, `mlserver` supports the deployment and serving of `lightgbm` models.
By default, it will assume that these models have been [serialised using the `bst.save_model()` method](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.Booster.html).

In this example, we will cover how we can train and serialise a simple model, to then serve it using `mlserver`.

## Training

To test the LightGBM Server, first we need to generate a simple LightGBM model using Python. 


```python
import lightgbm as lgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import os

model_dir = "."
BST_FILE = "iris-lightgbm.bst"

iris = load_iris()
y = iris['target']
X = iris['data']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
dtrain = lgb.Dataset(X_train, label=y_train)

params = {
    'objective':'multiclass', 
    'metric':'softmax',
    'num_class': 3
}
lgb_model = lgb.train(params=params, train_set=dtrain)
model_file = os.path.join(model_dir, BST_FILE)
lgb_model.save_model(model_file)
```

Our model will be persisted as a file named `iris-lightgbm.bst`.

## Serving

Now that we have trained and saved our model, the next step will be to serve it using `mlserver`. 
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
    "name": "iris-lgb",
    "implementation": "mlserver_lightgbm.LightGBMModel",
    "parameters": {
        "uri": "./iris-lightgbm.bst",
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

### Send test inference request

We now have our model being served by `mlserver`.
To make sure that everything is working as expected, let's send a request from our test set.

For that, we can use the Python types that `mlserver` provides out of box, or we can build our request manually.


```python
import requests

x_0 = X_test[0:1]
inference_request = {
    "inputs": [
        {
          "name": "predict-prob",
          "shape": x_0.shape,
          "datatype": "FP32",
          "data": x_0.tolist()
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/iris-lgb/versions/v0.1.0/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```

As we can see above, the model predicted the probability for each class, and the probability of class `1` is the biggest, close to `0.99`, which matches what's on the test set.


```python
y_test[0]
```
