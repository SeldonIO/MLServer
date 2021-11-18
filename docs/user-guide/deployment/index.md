# Deployment

MLServer is currently used as the core Python inference server in some of most
popular Kubernetes-native serving frameworks, including [Seldon
Core](https://docs.seldon.io/projects/seldon-core/en/latest/graph/protocols.html#v2-kfserving-protocol)
and [KServe (formerly known as
KFServing)](https://kserve.github.io/website/modelserving/v1beta1/sklearn/v2/).
This allows MLServer users to leverage the usability and maturity of these
frameworks to take their model deployments to the next level of their MLOps
journey, ensuring that they are served in a robust and scalable infrastructure.

```{note}
In general, it should be possible to deploy models using MLServer into **any
serving engine compatible with the V2 protocol**.
Alternatively, it's also possible to manage MLServer deployments manually as
regular processes (i.e. in a non-Kubernetes-native way).
However, this may be more involved and highly dependant on the deployment
infrastructure.
```

````{panels}
:img-top-cls: pl-5 pr-5 pt-5
:footer: text-center
:column: col-md-6

:img-top: ../../assets/seldon-core-logo.png

+++

```{link-button} ./seldon-core
:type: ref
:text: Deploy to Seldon Core
:classes: stretched-link
```
---
:img-top: ../../assets/kserve-logo.png

+++

```{link-button} ./kserve
:type: ref
:text: Deploy to KServe
:classes: stretched-link
```
````

```{toctree}
:hidden:
:titlesonly:
:maxdepth: 1

./seldon-core.md
./kserve.md
```
