# Deployment with KServe

MLServer is used as the [core Python inference server](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/) in
[KServe (formerly known as KFServing)](https://kserve.github.io/website/).
This allows for a straightforward avenue to deploy your models into a scalable
serving infrastructure backed by Kubernetes.

{% hint style="info" %}
This section assumes a basic knowledge of KServe and Kubernetes, as well as
access to a working Kubernetes cluster with KServe installed.
To learn more about [KServe](https://kserve.github.io/website/) or 
[how to install it](https://kserve.github.io/website/get_started/), please visit the
[KServe documentation](https://kserve.github.io/website/).
{% endhint %}

## Serving Runtimes

KServe provides built-in [serving runtimes](https://kserve.github.io/website/modelserving/v1beta1/serving_runtime/)
to deploy models trained in common ML frameworks. These allow you to deploy your models 
into a robust infrastructure by just pointing to where the model artifacts are stored remotely.

Some of these runtimes leverage MLServer as the core inference server.
Therefore, it should be straightforward to move from your local testing to your
serving infrastructure.

### Usage

To use any of the built-in serving runtimes offered by KServe, it should be
enough to select the relevant one your `InferenceService` manifest.

For example, to serve a Scikit-Learn model, you could use a manifest like the
one below:

```yaml
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
- The model will be served using the [V2 inference protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html),
  which can be enabled by setting the `protocolVersion` field to `v2`.

Once you have your `InferenceService` manifest ready, then the next step is to
apply it to your cluster.
There are multiple ways to do this, but the simplest is probably to just apply
it directly through `kubectl`, by running:

```bash
kubectl apply -f my-inferenceservice-manifest.yaml
```

### Supported Serving Runtimes

As mentioned above, KServe offers support for built-in serving runtimes, some
of which leverage MLServer as the inference server.
Below you can find a table listing these runtimes, and the MLServer inference
runtime that they correspond to.

| Framework    | MLServer Runtime                           | KServe Serving Runtime | Documentation                                                                                |
| ------------ | ------------------------------------------ | ---------------------- | -------------------------------------------------------------------------------------------- |
| Scikit-Learn | [MLServer SKLearn](../../runtimes/sklearn.md) | `sklearn`   | [SKLearn Serving Runtime](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/) |
| XGBoost      | [MLServer XGBoost](../../runtimes/xgboost.md) | `xgboost`   | [XGBoost Serving Runtime](https://kserve.github.io/website/modelserving/v1beta1/xgboost/)    |

Note that, on top of the ones shown above (backed by MLServer), KServe also
provides a [wider set](https://kserve.github.io/website/modelserving/v1beta1/serving_runtime/) of
serving runtimes.
To see the full list, please visit the [KServe documentation](https://kserve.github.io/website/modelserving/v1beta1/serving_runtime/).

## Custom Runtimes

Sometimes, the serving runtimes built into KServe may not be enough for our use case.
The framework provided by MLServer makes it easy to [write custom runtimes](../../runtimes/custom.md), 
which can then get packaged up as images. These images then become self-contained model 
servers with your custom runtime. Therefore, it's easy to deploy them into your serving infrastructure leveraging
KServe support for [custom runtimes](https://kserve.github.io/website/modelserving/v1beta1/custom/custom_model/#deploy-the-custom-predictor-on-kserve).

### Usage

The `InferenceService` manifest gives you full control over the containers used
to deploy your machine learning model. This can be leveraged to point your deployment to the 
[custom MLServer image containing your custom logic](../../runtimes/custom.md).
For example, if we assume that our custom image has been tagged as
`my-custom-server:0.1.0`, we could write an `InferenceService` manifest like
the one below:

```yaml
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
- Explicitly choosing the [V2 inference protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html) to
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
