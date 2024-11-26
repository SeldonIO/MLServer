# Serving a custom model

The `mlserver` package comes with inference runtime implementations for `scikit-learn` and `xgboost` models.
However, some times we may also need to roll out our own inference server, with custom logic to perform inference.
To support this scenario, MLServer makes it really easy to create your own extensions, which can then be containerised and deployed in a production environment.

## Overview

In this example, we will train a [`numpyro` model](http://num.pyro.ai/en/stable/).
The `numpyro` library streamlines the implementation of probabilistic models, abstracting away advanced inference and training algorithms.

Out of the box, `mlserver` doesn't provide an inference runtime for `numpyro`.
However, through this example we will see how easy is to develop our own.

## Training

The first step will be to train our model.
This will be a very simple bayesian regression model, based on an example provided in the [`numpyro` docs](https://nbviewer.jupyter.org/github/pyro-ppl/numpyro/blob/master/notebooks/source/bayesian_regression.ipynb).

Since this is a probabilistic model, during training we will compute an approximation to the posterior distribution of our model using MCMC.

```python
# Original source code and more details can be found in:
# https://nbviewer.jupyter.org/github/pyro-ppl/numpyro/blob/master/notebooks/source/bayesian_regression.ipynb


import numpyro
import numpy as np
import pandas as pd

from numpyro import distributions as dist
from jax import random
from numpyro.infer import MCMC, NUTS

DATASET_URL = "https://raw.githubusercontent.com/rmcelreath/rethinking/master/data/WaffleDivorce.csv"
dset = pd.read_csv(DATASET_URL, sep=";")

standardize = lambda x: (x - x.mean()) / x.std()

dset["AgeScaled"] = dset.MedianAgeMarriage.pipe(standardize)
dset["MarriageScaled"] = dset.Marriage.pipe(standardize)
dset["DivorceScaled"] = dset.Divorce.pipe(standardize)


def model(marriage=None, age=None, divorce=None):
    a = numpyro.sample("a", dist.Normal(0.0, 0.2))
    M, A = 0.0, 0.0
    if marriage is not None:
        bM = numpyro.sample("bM", dist.Normal(0.0, 0.5))
        M = bM * marriage
    if age is not None:
        bA = numpyro.sample("bA", dist.Normal(0.0, 0.5))
        A = bA * age
    sigma = numpyro.sample("sigma", dist.Exponential(1.0))
    mu = a + M + A
    numpyro.sample("obs", dist.Normal(mu, sigma), obs=divorce)


# Start from this source of randomness. We will split keys for subsequent operations.
rng_key = random.PRNGKey(0)
rng_key, rng_key_ = random.split(rng_key)

num_warmup, num_samples = 1000, 2000

# Run NUTS.
kernel = NUTS(model)
mcmc = MCMC(kernel, num_warmup=num_warmup, num_samples=num_samples)
mcmc.run(
    rng_key_, marriage=dset.MarriageScaled.values, divorce=dset.DivorceScaled.values
)
mcmc.print_summary()
```

### Saving our trained model

Now that we have _trained_ our model, the next step will be to save it so that it can be loaded afterwards at serving-time.
Note that, since this is a probabilistic model, we will only need to save the traces that approximate the posterior distribution over latent parameters.

This will get saved in a `numpyro-divorce.json` file.

```python
import json

samples = mcmc.get_samples()
serialisable = {}
for k, v in samples.items():
    serialisable[k] = np.asarray(v).tolist()

model_file_name = "numpyro-divorce.json"
with open(model_file_name, "w") as model_file:
    json.dump(serialisable, model_file)
```

## Serving

The next step will be to serve our model using `mlserver`.
For that, we will first implement an extension which serve as the _runtime_ to perform inference using our custom `numpyro` model.

### Custom inference runtime

Our custom inference wrapper should be responsible of:

- Loading the model from the set samples we saved previously.
- Running inference using our model structure, and the posterior approximated from the samples.

```python
# %load models.py
import json
import numpyro
import numpy as np

from jax import random
from mlserver import MLModel
from mlserver.codecs import decode_args
from mlserver.utils import get_model_uri
from numpyro.infer import Predictive
from numpyro import distributions as dist
from typing import Optional


class NumpyroModel(MLModel):
    async def load(self) -> bool:
        model_uri = await get_model_uri(self._settings)
        with open(model_uri) as model_file:
            raw_samples = json.load(model_file)

        self._samples = {}
        for k, v in raw_samples.items():
            self._samples[k] = np.array(v)

        self._predictive = Predictive(self._model, self._samples)

        return True

    @decode_args
    async def predict(
        self,
        marriage: Optional[np.ndarray] = None,
        age: Optional[np.ndarray] = None,
        divorce: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        predictions = self._predictive(
            rng_key=random.PRNGKey(0), marriage=marriage, age=age, divorce=divorce
        )

        obs = predictions["obs"]
        obs_mean = obs.mean()

        return np.asarray(obs_mean)

    def _model(self, marriage=None, age=None, divorce=None):
        a = numpyro.sample("a", dist.Normal(0.0, 0.2))
        M, A = 0.0, 0.0
        if marriage is not None:
            bM = numpyro.sample("bM", dist.Normal(0.0, 0.5))
            M = bM * marriage
        if age is not None:
            bA = numpyro.sample("bA", dist.Normal(0.0, 0.5))
            A = bA * age
        sigma = numpyro.sample("sigma", dist.Exponential(1.0))
        mu = a + M + A
        numpyro.sample("obs", dist.Normal(mu, sigma), obs=divorce)

```

### Settings files

The next step will be to create 2 configuration files:

- `settings.json`: holds the configuration of our server (e.g. ports, log level, etc.).
- `model-settings.json`: holds the configuration of our model (e.g. input type, runtime to use, etc.).

#### `settings.json`

```python
# %load settings.json
{
    "debug": "true"
}

```

#### `model-settings.json`

```python
# %load model-settings.json
{
    "name": "numpyro-divorce",
    "implementation": "models.NumpyroModel",
    "parameters": {
        "uri": "./numpyro-divorce.json"
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
import numpy as np

from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyCodec

x_0 = np.array([28.0])
inference_request = InferenceRequest(
    inputs=[
        NumpyCodec.encode_input(name="marriage", payload=x_0)
    ]
)

endpoint = "http://localhost:8080/v2/models/numpyro-divorce/infer"
response = requests.post(endpoint, json=inference_request.model_dump())

response.json()
```

## Deployment

Now that we have written and tested our custom model, the next step is to deploy it.
With that goal in mind, the rough outline of steps will be to first build a custom image containing our code, and then deploy it.

### Specifying requirements

MLServer will automatically find your requirements.txt file and install necessary python packages

```python
# %load requirements.txt
numpy==1.22.4
numpyro==0.8.0
jax==0.2.24
jaxlib==0.3.7

```

### Building a custom image

```{note}
This section expects that Docker is available and running in the background.
```

MLServer offers helpers to build a custom Docker image containing your code.
In this example, we will use the `mlserver build` subcommand to create an image, which we'll be able to deploy later.

Note that this section expects that Docker is available and running in the background, as well as a functional cluster with Seldon Core installed and some familiarity with `kubectl`.

```bash
%%bash
mlserver build . -t 'my-custom-numpyro-server:0.1.0'
```

To ensure that the image is fully functional, we can spin up a container and then send a test request. To start the container, you can run something along the following lines in a separate terminal:

```bash
docker run -it --rm -p 8080:8080 my-custom-numpyro-server:0.1.0
```

```python
import numpy as np

from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyCodec

x_0 = np.array([28.0])
inference_request = InferenceRequest(
    inputs=[
        NumpyCodec.encode_input(name="marriage", payload=x_0)
    ]
)

endpoint = "http://localhost:8080/v2/models/numpyro-divorce/infer"
response = requests.post(endpoint, json=inference_request.model_dump())

response.json()
```

As we should be able to see, the server running within our Docker image responds as expected.

### Deploying our custom image

```{note}
This section expects access to a functional Kubernetes cluster with Seldon Core installed and some familiarity with `kubectl`.
```

Now that we've built a custom image and verified that it works as expected, we can move to the next step and deploy it.
There is a large number of tools out there to deploy images.
However, for our example, we will focus on deploying it to a cluster running [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/).

```{note}
Also consider that depending on your Kubernetes installation Seldon Core might expect to get the container image from a public container registry like [Docker hub](https://hub.docker.com/) or [Google Container Registry](https://cloud.google.com/container-registry). For that you need to do an extra step of pushing the container to the registry using `docker tag <image name> <container registry>/<image name>` and `docker push <container registry>/<image name>` and also updating the `image` section of the yaml file to `<container registry>/<image name>`.
```

For that, we will need to create a `SeldonDeployment` resource which instructs Seldon Core to deploy a model embedded within our custom image and compliant with the [V2 Inference Protocol](https://github.com/kserve/kserve/tree/master/docs/predict-api/v2).
This can be achieved by _applying_ (i.e. `kubectl apply`) a `SeldonDeployment` manifest to the cluster, similar to the one below:

```python
%%writefile seldondeployment.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: numpyro-model
spec:
  protocol: v2
  predictors:
    - name: default
      graph:
        name: numpyro-divorce
        type: MODEL
      componentSpecs:
        - spec:
            containers:
              - name: numpyro-divorce
                image: my-custom-numpyro-server:0.1.0
```

```python

```
