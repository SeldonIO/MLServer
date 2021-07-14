# Serving MLflow models

Out of the box, MLServer supports the deployment and serving of MLflow models with the following features:

- Loading of MLflow Model artifacts.
- Support of dataframes, dict-of-tensors and tensor inputs.

In this example, we will showcase some of this features using an example model.


```python
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))
```

## Training

The first step will be to train and serialise a MLflow model.
For that, we will use the [linear regression examle from the MLflow docs](https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html).


```python
# %load src/train.py
# Original source code and more details can be found in:
# https://www.mlflow.org/docs/latest/tutorials-and-examples/tutorial.html

# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s",
            e,
        )

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                lr, "model", registered_model_name="ElasticnetWineModel"
            )
        else:
            mlflow.sklearn.log_model(lr, "model")

```


```python
!python src/train.py
```

The training script will also serialise our trained model, leveraging the [MLflow Model format](https://www.mlflow.org/docs/latest/models.html).
By default, we should be able to find the saved artifact under the `mlruns` folder.


```python
[experiment_file_path] = !ls -td ./mlruns/0/* | head -1
model_path = os.path.join(experiment_file_path, "artifacts", "model")
print(model_path)
```


```python
!ls {model_path} 
```

## Serving

Now that we have trained and serialised our model, we are ready to start serving it.
For that, the initial step will be to set up a `model-settings.json` that instructs MLServer to load our artifact using the MLflow Inference Runtime.


```python
%%writetemplate ./model-settings.json
{{
    "name": "wine-classifier",
    "implementation": "mlserver_mlflow.MLflowRuntime",
    "parameters": {{
        "uri": "{model_path}"
    }}
}}
```

Now that we have our config in-place, we can start the server by running `mlserver start .`. This needs to either be ran from the same directory where our config files are or pointing to the folder where they are.

```shell
mlserver start .
```

Since this command will start the server and block the terminal, waiting for requests, this will need to be ran in the background on a separate terminal.

### Send test inference request

We now have our model being served by `mlserver`.
To make sure that everything is working as expected, let's send a request from our test set.
For that, we can use the Python types that `mlserver` provides out of box, or we can build our request manually.

Note that, the request specifies the value `pd` as its *content type*, whereas every input specifies the *content type* `np`.
These parameters will instruct MLServer to:

- Convert every input value to a NumPy array, using the data type and shape information provided.
- Group all the different inputs into a Pandas DataFrame, using their names as the column names.

To learn more about how MLServer uses content type parameters, you can check this [worked out example](../content-type/README.md).


```python
import requests

inference_request = {
    "parameters": {
        "content_type": "pd"
    },
    "inputs": [
        {
          "name": "fixed acidity",
          "shape": [1],
          "datatype": "FP32",
          "data": [7.4],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "volatile acidity",
          "shape": [1],
          "datatype": "FP32",
          "data": [0.7000],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "citric acidity",
          "shape": [1],
          "datatype": "FP32",
          "data": [0],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "residual sugar",
          "shape": [1],
          "datatype": "FP32",
          "data": [1.9],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "chlorides",
          "shape": [1],
          "datatype": "FP32",
          "data": [0.076],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "free sulfur dioxide",
          "shape": [1],
          "datatype": "FP32",
          "data": [11],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "total sulfur dioxide",
          "shape": [1],
          "datatype": "FP32",
          "data": [34],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "density",
          "shape": [1],
          "datatype": "FP32",
          "data": [0.9978],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "pH",
          "shape": [1],
          "datatype": "FP32",
          "data": [3.51],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "sulphates",
          "shape": [1],
          "datatype": "FP32",
          "data": [0.56],
          "parameters": {
              "content_type": "np"
          }
        },
        {
          "name": "alcohol",
          "shape": [1],
          "datatype": "FP32",
          "data": [9.4],
          "parameters": {
              "content_type": "np"
          }
        },
    ]
}

endpoint = "http://localhost:8080/v2/models/wine-classifier/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```

As we can see in the output above, the predicted quality score for our input wine was `5.57`.

### MLflow Scoring Protocol

MLflow currently ships with an [scoring server with its own protocol](https://www.mlflow.org/docs/latest/models.html#deploy-mlflow-models).
In order to provide a drop-in replacement, the MLflow runtime in MLServer also exposes a custom endpoint which matches the signature of the MLflow's `/invocations` endpoint.

As an example, we can try to send a request using MLflow's protocol to our running MLServer instance.


```python
import requests

inference_request = {
    "columns": [
        "alcohol",
        "chlorides",
        "citric acid",
        "density",
        "fixed acidity",
        "free sulfur dioxide",
        "pH",
        "residual sugar",
        "sulphates",
        "total sulfur dioxide",
        "volatile acidity",
    ],
    "data": [[7.4,0.7,0,1.9,0.076,11,34,0.9978,3.51,0.56,9.4]],
}

endpoint = "http://localhost:8080/invocations"
response = requests.post(endpoint, json=inference_request)

response.json()
```

As we can see above, the predicted quality for our input is `5.57`, matching the prediction we obtained above.
