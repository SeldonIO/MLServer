# Deployment

MLServer is currently used as the core Python inference server in some of most popular Kubernetes-native serving frameworks, including [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/graph/protocols.html#v2-kfserving-protocol) and [KServe (formerly known as KFServing)](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/). This allows MLServer users to leverage the usability and maturity of these frameworks to take their model deployments to the next level of their MLOps journey, ensuring that they are served in a robust and scalable infrastructure.

{% hint style="info" %}
{% code overflow="wrap" %}
```
In general, it should be possible to deploy models using MLServer into **any serving engine compatible with the V2 protocol**. Alternatively, it's also possible to manage MLServer deployments manually as regular processes (i.e. in a non-Kubernetes-native way). However, this may be more involved and highly dependant on the deployment infrastructure.
```
{% endcode %}
{% endhint %}

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td></td><td>Seldon Core</td><td></td><td><a href="seldon-core.md">seldon-core.md</a></td><td><a href="../../.gitbook/assets/seldon-core-logo.png">seldon-core-logo.png</a></td></tr><tr><td></td><td>KServe</td><td></td><td><a href="kserve.md">kserve.md</a></td><td><a href="../../.gitbook/assets/kserve-logo.png">kserve-logo.png</a></td></tr></tbody></table>
