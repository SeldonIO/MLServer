# Deployment to KServe

MLServer is used as the [core Python inference
server](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/) in
[KServe (formerly known as KFServing)](https://kserve.github.io/website/).
Therefore, this allows for an easier integration between your local and remote
environments.

```{note}
This section assumes a basic knowledge of KServe and Kubernetes, as well as
access to a working Kubernetes cluster with KServe installed.
To learn more about [KServe](https://kserve.github.io/website/) or [how to
install it](https://kserve.github.io/website/get_started/), please visit the
[KServe documentation](https://kserve.github.io/).
```

## Serving Runtimes

KServe provides built-in [serving
runtimes](https://kserve.github.io/website/modelserving/v1beta1/serving_runtime/)
to deploy models trained in common ML frameworks.
These allow you to deploy your models by just pointing to where the model
artifacts are stored remotely.

Some of these runtimes leverage MLServer as the core inference server.
Therefore, it should be straightforward to move them from your local testing to
your serving infrastructure.

### Usage

To use any of the built-in serving runtimes offered by KServe, it should be
enough to select any of the available ones on your `InferenceService` manifest.

For example, to serve a Scikit-Learn model, you could use a manifest like the
one below:

```{code-block} yaml
---
emphasize-lines: 7, 8
---
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: my-model
spec:
  predictor:
    sklearn:
      protocolVersion: v2
      storageUri: gs://seldon-models/sklearn/iris
```

As you can see highlighted above, the `InferenceService` manifest will only
need to specify the following points:

- The model artifact is a Scikit-Learn model. Therefore, we will use the
  `sklearn` serving runtime to deploy it.
- The model will be served using the [V2 inference
  protocol](https://kserve.github.io/website/modelserving/inference_api/),
  which can be enabled by setting the `protocolVersion` field to `v2`.

Once you have your `InferenceService` manifest ready, then the next step is to
apply it to your cluster.
There are multiple ways to do this, but the simplest is probably to just apply
it directly through `kubectl`, by running:

```bash
kubectl apply -f my-inferenceservice-manifest.yaml
```

### Supported Serving Runtimes

As mentioned above, KServe supports a limited number of serving runtimes
out-of-the-box, some of which leverage MLServer as the inference server.
Below you can find a table listing these runtimes, and the MLServer inference
runtime that they correspond to.

| Framework    | MLServer Runtime                           | KServe Serving Runtime | Documentation                                                                                |
| ------------ | ------------------------------------------ | ---------------------- | -------------------------------------------------------------------------------------------- |
| Scikit-Learn | [MLServer SKLearn](../../runtimes/sklearn) | `sklearn`              | [SKLearn Serving Runtime](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/) |
| XGBoost      | [MLServer XGBoost](../../runtimes/xgboost) | `xgboost`              | [XGBoost Serving Runtime](https://kserve.github.io/website/modelserving/v1beta1/xgboost/)    |

## Custom Images

Some times, the serving runtimes built into KServe may not be enough for
our use case.
The framework provided by MLServer makes it easy to [write custom
runtimes](../../runtimes/custom), which can then get packaged up as images.
These images then become self-contained model servers with your custom runtime,
which can be easily deployed by KServe into your serving infrastructure.

### Usage

The `InferenceService` manifest gives you full control over the containers used
to deploy your machine learning model.
This can be leveraged to poing your deployment to the [custom MLServer image
containing your custom logic](../../runtimes/custom).
For example, if we assume that our custom image has been tagged as
`my-custom-server:0.1.0`, we could write an `InferenceService` manifest like
the one below:

```{code-block} yaml
---
emphasize-lines: 9, 11-12, 13-15
---
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: my-model
spec:
  predictor:
    containers:
      - name: classifier
        image: my-custom-server:0.1.0
        env:
          - name: PROTOCOL
            value: v2
        ports:
          - containerPort: 8080
            protocol: TCP
```

As we can see highlighted above, the main points that we'll need to take into
account are:

- Pointing to our custom MLServer `image` in the custom container section of
  our `InferenceService`.
- Explicitly choosing the [v2 inference
  protocol](https://kserve.github.io/website/modelserving/inference_api/) to
  serve our model.
- Let KServe know what port will be exposed by our custom container to send
  inference requests.

Once you have your `InferenceService` manifest ready, then the next step is to
apply it to your cluster.
There are multiple ways to do this, but the simplest is probably to just apply
it directly through `kubectl`, by running:

```bash
kubectl apply -f my-inferenceservice-manifest.yaml
```
