# Deployment with Seldon Core

MLServer is used as the [core Python inference server](https://docs.seldon.io/projects/seldon-core/en/latest/graph/protocols.html#v2-kfserving-protocol)
in [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/index.html).
Therefore, it should be straightforward to deploy your models either by using one of the 
[built-in pre-packaged servers](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/overview.html#two-types-of-model-servers)
or by pointing to a [custom image of MLServer](../../runtimes/custom.md).

{% hint style="info" %}
This section assumes a basic knowledge of Seldon Core and Kubernetes, as well
as access to a working Kubernetes cluster with Seldon Core installed.
To learn more about [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/) or 
[how to install it](https://docs.seldon.io/projects/seldon-core/en/latest/nav/installation.html),
please visit the [Seldon Core documentation](https://docs.seldon.io/projects/seldon-core/en/latest/index.html).
{% endhint %}

## Pre-packaged Servers

Out of the box, Seldon Core comes a few MLServer runtimes pre-configured to run straight away.
This allows you to deploy a MLServer instance by just pointing to where your
model artifact is and specifying what ML framework was used to train it.

### Usage

To let Seldon Core know what framework was used to train your model, you can
use the `implementation` field of your `SeldonDeployment` manifest.
For example, to deploy a Scikit-Learn artifact stored remotely in GCS, one
could do:

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: my-model
spec:
  protocol: v2
  predictors:
    - name: default
      graph:
        name: classifier
        implementation: SKLEARN_SERVER
        modelUri: gs://seldon-models/sklearn/iris
```

As you can see highlighted above, all that we need to specify is that:

- Our **inference deployment should use the [V2 inference protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html)**,
  which is done by **setting the `protocol` field to `kfserving`**.
- Our **model artifact is a serialised Scikit-Learn model**, therefore it
  should be served using the [MLServer SKLearn runtime](../../runtimes/sklearn.md),
  which is done by **setting the `implementation` field to `SKLEARN_SERVER`**.

Note that, while the `protocol` should always be set to `kfserving` (i.e. so
that models are served using the [V2 inference protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html)), the
value of the `implementation` field will be dependant on your ML framework.
The valid values of the `implementation` field are [pre-determined by Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/graph/protocols.html#v2-kfserving-protocol).
However, it should also be possible to [configure and add new ones](https://docs.seldon.io/projects/seldon-core/en/latest/servers/custom.html#adding-a-new-inference-server)
(e.g. to support a [custom MLServer runtime](../../runtimes/custom.md)).

Once you have your `SeldonDeployment` manifest ready, then the next step is to
apply it to your cluster.
There are multiple ways to do this, but the simplest is probably to just apply
it directly through `kubectl`, by running:

```bash
kubectl apply -f my-seldondeployment-manifest.yaml
```

To consult the supported values of the `implementation` field where MLServer is
used, you can check the support table below.

### Supported Pre-packaged Servers

As mentioned above, pre-packaged servers come built-in into Seldon Core.
Therefore, only a pre-determined subset of them will be supported for a given
release of Seldon Core.

The table below shows a list of the currently supported values of the
`implementation` field.
Each row will also show what ML framework they correspond to and also what
MLServer runtime will be enabled internally on your model deployment when used.

| Framework    | MLServer Runtime                                 | Seldon Core Pre-packaged Server | Documentation                                                                                |
| ------------ | ------------------------------------------------ | ------------------------------- | -------------------------------------------------------------------------------------------- |
| Scikit-Learn | [MLServer SKLearn](../../runtimes/sklearn.md)       | `SKLEARN_SERVER`                | [SKLearn Server](https://docs.seldon.io/projects/seldon-core/en/latest/servers/sklearn.html) |
| XGBoost      | [MLServer XGBoost](../../runtimes/xgboost.md)      | `XGBOOST_SERVER`                | [XGBoost Server](https://docs.seldon.io/projects/seldon-core/en/latest/servers/xgboost.html) |
| MLflow       | [MLServer MLflow](../../runtimes/mlflow.md)         | `MLFLOW_SERVER`                 | [MLflow Server](https://docs.seldon.io/projects/seldon-core/en/latest/servers/mlflow.html)   |

Note that, on top of the ones shown above (backed by MLServer), Seldon Core
**also provides a [wider set](https://docs.seldon.io/projects/seldon-core/en/latest/nav/config/servers.html)**
of pre-packaged servers. To check the full list, please visit the 
[Seldon Core documentation](https://docs.seldon.io/projects/seldon-core/en/latest/nav/config/servers.html).

## Custom Runtimes

There could be cases where the pre-packaged MLServer runtimes supported
out-of-the-box in Seldon Core may not be enough for our use case.
The framework provided by MLServer makes it easy to [write custom runtimes](../../runtimes/custom.md), 
which can then get packaged up as images. These images then become self-contained 
model servers with your custom runtime. Therefore Seldon Core makes it as easy 
to deploy them into your serving infrastructure.

### Usage

The `componentSpecs` field of the `SeldonDeployment` manifest will allow us to
let Seldon Core know what image should be used to serve a custom model.
For example, if we assume that our custom image has been tagged as
`my-custom-server:0.1.0`, we could write our `SeldonDeployment` manifest as
follows:

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: my-model
spec:
  protocol: v2
  predictors:
    - name: default
      graph:
        name: classifier
      componentSpecs:
        - spec:
            containers:
              - name: classifier
                image: my-custom-server:0.1.0
```

As we can see highlighted on the snippet above, all that's needed to deploy a
custom MLServer image is:

- Letting Seldon Core know that the model deployment will be served through the
  [V2 inference protocol](https://docs.seldon.io/projects/seldon-core/en/latest/reference/apis/v2-protocol.html)) by
  setting the `protocol` field to `v2`.
- Pointing our model container to use our **custom MLServer image**, by
  specifying it on the `image` field of the `componentSpecs` section of the
  manifest.

Once you have your `SeldonDeployment` manifest ready, then the next step is to
apply it to your cluster.
There are multiple ways to do this, but the simplest is probably to just apply
it directly through `kubectl`, by running:

```bash
kubectl apply -f my-seldondeployment-manifest.yaml
```
