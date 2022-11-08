# Custom Conda environments in MLServer

It's not unusual that model runtimes require extra dependencies that are not direct dependencies of MLServer.
This is the case when we want to use [custom runtimes](../custom/README), but also when our model artifacts are the output of older versions of a toolkit (e.g. models trained with an older version of SKLearn).

In these cases, since these dependencies (or dependency versions) are not known in advance by MLServer, they **won't be included in the default `seldonio/mlserver` Docker image**.
To cover these cases, the **`seldonio/mlserver` Docker image allows you to load custom environments** before starting the server itself.

This example will walk you through how to create and save an custom environment, so that it can be loaded in MLServer without any extra change to the `seldonio/mlserver` Docker image. 

## Define our environment

For this example, we will create a custom environment to serve a model trained with an older version of Scikit-Learn. 
The first step will be define this environment, using a [`environment.yml`](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually). 

Note that these environments can also be created on the fly as we go, and then serialised later.


```python
%%writefile environment.yml

name: old-sklearn
channels:
    - conda-forge
dependencies:
    - python == 3.8
    - scikit-learn == 0.24.2
    - joblib == 0.17.0
    - requests
    - pip
    - pip:
        - mlserver == 1.1.0
        - mlserver-sklearn == 1.1.0
```

### Train model in our custom environment

To illustrate the point, we will train a Scikit-Learn model using our older environment.

The first step will be to create and activate an environment which reflects what's outlined in our `environment.yml` file.

> **NOTE:** If you are running this from a Jupyter Notebook, you will need to restart your Jupyter instance so that it runs from this environment.


```python
!conda env create --force -f environment.yml
!conda activate old-sklearn
```

We can now train and save a Scikit-Learn model using the older version of our environment.
This model will be serialised as `model.joblib`.

You can find more details of this process in the [Scikit-Learn example](../sklearn/README).


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
X_train, X_test, y_train, y_test = train_test_split(
    data, digits.target, test_size=0.5, shuffle=False)

# We learn the digits on the first half of the digits
classifier.fit(X_train, y_train)
```


```python
import joblib

model_file_name = "model.joblib"
joblib.dump(classifier, model_file_name)
```

### Serialise our custom environment

Lastly, we will need to serialise our environment in the format expected by MLServer.
To do that, we will use a tool called [`conda-pack`](https://conda.github.io/conda-pack/).

This tool, will save a portable version of our environment as a `.tar.gz` file, also known as _tarball_.


```python
!conda pack --force -n old-sklearn -o old-sklearn.tar.gz
```

## Serving 

Now that we have defined our environment (and we've got a sample artifact trained in that environment), we can move to serving our model.

To do that, we will first need to select the right runtime through a `model-settings.json` config file.


```python
%%writefile model-settings.json
{
    "name": "mnist-svm",
    "implementation": "mlserver_sklearn.SKLearnModel"
}
```

We can then spin up our model, using our custom environment, leveraging MLServer's Docker image.
Keep in mind that **you will need Docker installed in your machine to run this example**.

Our Docker command will need to take into account the following points:

- Mount the example's folder as a volume so that it can be accessed from within the container.
- Let MLServer know that our custom environment's tarball can be found as `old-sklearn.tar.gz`.
- Expose port `8080` so that we can send requests from the outside. 

From the command line, this can be done using Docker's CLI as:

```bash
docker run -it --rm \
    -v "$PWD":/mnt/models \
    -e "MLSERVER_ENV_TARBALL=/mnt/models/old-sklearn.tar.gz" \
    -p 8080:8080 \
    seldonio/mlserver:1.1.0-slim
```

Note that we need to keep the server running in the background while we send requests.
Therefore, it's best to run this command on a separate terminal session.

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
          "name": "predict",
          "shape": x_0.shape,
          "datatype": "FP32",
          "data": x_0.tolist()
        }
    ]
}

endpoint = "http://localhost:8080/v2/models/mnist-svm/infer"
response = requests.post(endpoint, json=inference_request)

response.json()
```


```python

```
