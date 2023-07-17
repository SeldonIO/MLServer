# Changelog


<a name="1.3.5"></a>
## [1.3.5](https://github.com/SeldonIO/MLServer/releases/tag/1.3.5) - 10 Jul 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.3.5 -->

### What's Changed

* Rename HF codec to `hf` by [@adriangonz](https://github.com/adriangonz)  in https://github.com/SeldonIO/MLServer/pull/1268
* Publish is_drift metric to Prom by [@joshsgoldstein](https://github.com/joshsgoldstein)  in https://github.com/SeldonIO/MLServer/pull/1263

### New Contributors
* [@joshsgoldstein](https://github.com/joshsgoldstein) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1263

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.4...1.3.5

[Changes][1.3.5]


<a name="1.3.4"></a>
## [1.3.4](https://github.com/SeldonIO/MLServer/releases/tag/1.3.4) - 21 Jun 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.3.4 -->

### What's Changed

* Silent logging by [@dtpryce](https://github.com/dtpryce) in https://github.com/SeldonIO/MLServer/pull/1230
* Fix `mlserver infer` with `BYTES` by [@RafalSkolasinski](https://github.com/RafalSkolasinski) in https://github.com/SeldonIO/MLServer/pull/1213

### New Contributors
* [@dtpryce](https://github.com/dtpryce) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1230

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.3...1.3.4

[Changes][1.3.4]


<a name="1.3.3"></a>
## [1.3.3](https://github.com/SeldonIO/MLServer/releases/tag/1.3.3) - 05 Jun 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.3.3 -->

### What's Changed

* Add default LD_LIBRARY_PATH env var by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1120
* Adding cassava tutorial (mlserver + seldon core) by [@edshee](https://github.com/edshee) in https://github.com/SeldonIO/MLServer/pull/1156
* Add docs around converting to / from JSON by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1165
* Document SKLearn available outputs by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1167 
* Fix minor typo in `alibi-explain` tests by [@ascillitoe](https://github.com/ascillitoe) in https://github.com/SeldonIO/MLServer/pull/1170
* Add support for `.ubj` models and improve XGBoost docs by [@adriangonz](https://github.com/adriangonz) in  https://github.com/SeldonIO/MLServer/pull/1168
* Fix content type annotations for pandas codecs by [@adriangonz](https://github.com/adriangonz) in  https://github.com/SeldonIO/MLServer/pull/1162
* Added option to configure the grpc histogram by [@cristiancl25](https://github.com/cristiancl25) in https://github.com/SeldonIO/MLServer/pull/1143
* Add OS classifiers to project's metadata by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1171
* Don't use `qsize` for parallel worker queue by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1169
* Fix small typo in Python API docs by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc)  in https://github.com/SeldonIO/MLServer/pull/1174
* Fix star import in `mlserver.codecs.*` by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1172

### New Contributors
* [@cristiancl25](https://github.com/cristiancl25) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1143
* [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1174

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.2...1.3.3

[Changes][1.3.3]


<a name="1.3.2"></a>
## [1.3.2](https://github.com/SeldonIO/MLServer/releases/tag/1.3.2) - 10 May 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.4.0.dev2 -->

### What's Changed
* Use default initialiser if not using a custom env by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1104
* Add support for online drift detectors by [@ascillitoe](https://github.com/ascillitoe) in https://github.com/SeldonIO/MLServer/pull/1108
* added intera and inter op parallelism parameters to the hugggingface … by [@saeid93](https://github.com/saeid93) in https://github.com/SeldonIO/MLServer/pull/1081
* Fix settings reference in runtime docs by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1109
* Bump Alibi libs requirements by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1121
* Add default LD_LIBRARY_PATH env var by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1120
* Ignore both .metrics and .envs folders by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1132

### New Contributors
* [@ascillitoe](https://github.com/ascillitoe) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1108

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.1...1.3.2

[Changes][1.3.2]


<a name="1.3.1"></a>
## [1.3.1](https://github.com/SeldonIO/MLServer/releases/tag/1.3.1) - 27 Apr 2023

### What's Changed

- Move OpenAPI schemas into Python package ([#1095](https://github.com/SeldonIO/MLServer/issues/1095))

[Changes][1.3.1]


<a name="1.3.0"></a>
## [1.3.0](https://github.com/SeldonIO/MLServer/releases/tag/1.3.0) - 27 Apr 2023

> WARNING :warning: : The `1.3.0` has been yanked from PyPi due to a packaging issue. This should have been now resolved in `>= 1.3.1`. 

### What's Changed

#### Custom Model Environments

More often that not, your custom runtimes will depend on external 3rd party dependencies which are not included within the main MLServer package - or different versions of the same package (e.g. `scikit-learn==1.1.0` vs `scikit-learn==1.2.0`). In these cases, to load your custom runtime, MLServer will need access to these dependencies.

In MLServer `1.3.0`, it is now [possible to load this custom set of dependencies by providing them](https://mlserver.readthedocs.io/en/latest/user-guide/custom.html#loading-a-custom-python-environment), through an [environment tarball](https://mlserver.readthedocs.io/en/latest/examples/conda/README.html), whose path can be specified within your `model-settings.json` file. This custom environment will get provisioned on the fly after loading a model - alongside the default environment and any other custom environments.

Under the hood, each of these environments will run their own separate pool of workers.

![image](https://user-images.githubusercontent.com/1577620/234797983-aa52c353-2d2f-4261-a078-06bfe62cae87.png)

#### Custom Metrics

The MLServer framework now includes a simple interface that allows you to register and keep track of any [custom metrics](https://mlserver.readthedocs.io/en/latest/user-guide/metrics.html#custom-metrics):

- `[mlserver.register()](https://mlserver.readthedocs.io/en/latest/reference/api/metrics.html#mlserver.register)`: Register a new metric.
- `[mlserver.log()](https://mlserver.readthedocs.io/en/latest/reference/api/metrics.html#mlserver.log)`: Log a new set of metric / value pairs.

Custom metrics will generally be registered in the `[load()](https://mlserver.readthedocs.io/en/latest/reference/api/model.html#mlserver.MLModel.load)` method and then used in the `[predict()](https://mlserver.readthedocs.io/en/latest/reference/api/model.html#mlserver.MLModel.predict)` method of your [custom runtime](https://mlserver.readthedocs.io/en/latest/user-guide/custom.html). These metrics can then be polled and queried via [Prometheus](https://mlserver.readthedocs.io/en/latest/user-guide/metrics.html#settings).

![image](https://user-images.githubusercontent.com/1577620/234798211-9e538439-4914-4aa6-9c3f-539a66e3ce54.png)

#### OpenAPI

MLServer `1.3.0` now includes an autogenerated Swagger UI which can be used to interact dynamically with the Open Inference Protocol.

The autogenerated Swagger UI can be accessed under the `/v2/docs` endpoint.

![https://mlserver.readthedocs.io/en/latest/_images/swagger-ui.png](https://mlserver.readthedocs.io/en/latest/_images/swagger-ui.png)

Alongside the [general API documentation](https://mlserver.readthedocs.io/en/latest/user-guide/openapi.html#Swagger-UI), MLServer also exposes now a set of API docs tailored to individual models, showing the specific endpoints available for each one.

The model-specific autogenerated Swagger UI can be accessed under the following endpoints:

- `/v2/models/{model_name}/docs`
- `/v2/models/{model_name}/versions/{model_version}/docs`

#### HuggingFace Improvements

MLServer now includes improved Codec support for all the main different types that can be returned by HugginFace models - ensuring that the values returned via the Open Inference Protocol are more semantic and meaningful.

Massive thanks to [@pepesi](https://github.com/pepesi)  for taking the lead on improving the HuggingFace runtime!

#### Support for Custom Model Repositories

Internally, MLServer leverages a Model Repository implementation which is used to discover and find different models (and their versions) available to load. The latest version of MLServer will now allow you to swap this for your own model repository implementation - letting you integrate against your own model repository workflows. 

This is exposed via the [model_repository_implementation](https://mlserver.readthedocs.io/en/latest/reference/settings.html#mlserver.settings.Settings.model_repository_implementation) flag of your `settings.json` configuration file. 

Thanks to [@jgallardorama](https://github.com/jgallardorama)  (aka [@jgallardorama-itx](https://github.com/jgallardorama-itx) ) for his effort contributing this feature!

#### Batch and Worker Queue Metrics

MLServer `1.3.0` introduces a [new set of metrics](https://mlserver.readthedocs.io/en/latest/user-guide/metrics.html#default-metrics) to increase visibility around two of its internal queues:

- [Adaptive batching](https://mlserver.readthedocs.io/en/latest/user-guide/adaptive-batching.html) queue: used to accumulate request batches on the fly.
- [Parallel inference](https://mlserver.readthedocs.io/en/latest/user-guide/parallel-inference.html) queue: used to send over requests to the inference worker pool.

Many thanks to [@alvarorsant](https://github.com/alvarorsant)  for taking the time to implement this highly requested feature!

#### Image Size Optimisations

The latest version of MLServer includes a few optimisations around image size, which help reduce the size of the official set of images by more than ~60% - making them more convenient to use and integrate within your workloads. In the case of the full `seldonio/mlserver:1.3.0` image (including all runtimes and dependencies), this means going from 10GB down to ~3GB.

#### Python API Documentation

Alongside its built-in inference runtimes, MLServer also exposes a Python framework that you can use to extend MLServer and write your own codecs and inference runtimes. The MLServer official docs now include a [reference page](https://mlserver.readthedocs.io/en/latest/reference/api/index.html) documenting the main components of this framework in more detail.

### New Contributors
* [@rio](https://github.com/rio) made their first contribution in https://github.com/SeldonIO/MLServer/pull/864
* [@pepesi](https://github.com/pepesi) made their first contribution in https://github.com/SeldonIO/MLServer/pull/692
* [@jgallardorama](https://github.com/jgallardorama) made their first contribution in https://github.com/SeldonIO/MLServer/pull/849
* [@alvarorsant](https://github.com/alvarorsant) made their first contribution in https://github.com/SeldonIO/MLServer/pull/860
* [@gawsoftpl](https://github.com/gawsoftpl) made their first contribution in https://github.com/SeldonIO/MLServer/pull/950
* [@stephen37](https://github.com/stephen37) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1033
* [@sauerburger](https://github.com/sauerburger) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1064

[Changes][1.3.0]


<a name="1.2.4"></a>
## [1.2.4](https://github.com/SeldonIO/MLServer/releases/tag/1.2.4) - 10 Mar 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.2.4 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.3...1.2.4

[Changes][1.2.4]


<a name="1.2.3"></a>
## [1.2.3](https://github.com/SeldonIO/MLServer/releases/tag/1.2.3) - 16 Jan 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.2.3 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.2...1.2.3

[Changes][1.2.3]


<a name="1.2.2"></a>
## [1.2.2](https://github.com/SeldonIO/MLServer/releases/tag/1.2.2) - 16 Jan 2023

<!-- Release notes generated using configuration in .github/release.yml at 1.2.2 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.1...1.2.2

[Changes][1.2.2]


<a name="1.2.1"></a>
## [1.2.1](https://github.com/SeldonIO/MLServer/releases/tag/1.2.1) - 19 Dec 2022

<!-- Release notes generated using configuration in .github/release.yml at 1.2.1 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.0...1.2.1

[Changes][1.2.1]


<a name="1.2.0"></a>
## [1.2.0](https://github.com/SeldonIO/MLServer/releases/tag/1.2.0) - 25 Nov 2022

<!-- Release notes generated using configuration in .github/release.yml at 1.2.0 -->

### What's Changed

#### Simplified Interface for Custom Runtimes

MLServer now exposes an alternative [_“simplified”_ interface](https://mlserver.readthedocs.io/en/latest/user-guide/custom.html#simplified-interface) which can be used to write custom runtimes. This interface can be enabled by decorating your predict() method with the `mlserver.codecs.decode_args` decorator, and it lets you specify in the method signature both how you want your request payload to be decoded and how to encode the response back.

Based on the information provided in the method signature, MLServer will automatically decode the request payload into the different inputs specified as keyword arguments. Under the hood, this is implemented through [MLServer’s codecs and content types system](https://mlserver.readthedocs.io/en/latest/user-guide/content-type.html).

```python
from mlserver import MLModel
from mlserver.codecs import decode_args

class MyCustomRuntime(MLModel):

  async def load(self) -> bool:
    # TODO: Replace for custom logic to load a model artifact
    self._model = load_my_custom_model()
    self.ready = True
    return self.ready

  @decode_args
  async def predict(self, questions: List[str], context: List[str]) -> np.ndarray:
    # TODO: Replace for custom logic to run inference
    return self._model.predict(questions, context)
```

#### Built-in Templates for Custom Runtimes

To make it easier to write your own custom runtimes, MLServer now ships with a `mlserver init` command that will generate a templated project. This project will include a skeleton with folders, unit tests, Dockerfiles, etc. for you to fill.

![image1](https://user-images.githubusercontent.com/1577620/203810614-f4daa32e-8b1d-4bea-9b02-959b1d054596.gif)

#### Dynamic Loading of Custom Runtimes

MLServer now lets you [load custom runtimes dynamically](https://mlserver.readthedocs.io/en/latest/user-guide/custom.html#loading-a-custom-mlserver-runtime) into a running instance of MLServer. Once you have your custom runtime ready, all you need to do is to move it to your model folder, next to your `model-settings.json` configuration file.

For example, if we assume a flat model repository where each folder represents a model, you would end up with a folder structure like the one below:

```
.
├── models
│   └── sum-model
│       ├── model-settings.json
│       ├── models.py
```

#### Batch Inference Client

This release of MLServer introduces a new [`mlserver infer`](https://mlserver.readthedocs.io/en/latest/reference/cli.html#mlserver-infer) command, which will let you run inference over a large batch of input data on the client side. Under the hood, this command will stream a large set of inference requests from specified input file, arrange them in microbatches, orchestrate the request / response lifecycle, and will finally write back the obtained responses into output file.

#### Parallel Inference Improvements

The `1.2.0` release of MLServer, includes a number of fixes around the parallel inference pool focused on improving the architecture to optimise memory usage and reduce latency. These changes include (but are not limited to):

- The main MLServer process won’t load an extra replica of the model anymore. Instead, all computing will occur on the parallel inference pool.
- The worker pool will now ensure that all requests are executed on each worker’s AsyncIO loop, thus optimising compute time vs IO time.
- Several improvements around logging from the inference workers. 

#### Dropped support for Python 3.7

MLServer has now dropped support for Python `3.7`. Going forward, only `3.8`, `3.9` and `3.10` will be supported (with `3.8` being used in our official set of images).

#### Move to UBI Base Images

The official set of MLServer images has now moved to use [UBI 9](https://www.redhat.com/en/blog/introducing-red-hat-universal-base-image) as a base image. This ensures support to run MLServer in OpenShift clusters, as well as a well-maintained baseline for our images. 

#### Support for MLflow 2.0

In line with MLServer’s close relationship with the MLflow team, this release of MLServer introduces support for the recently released MLflow 2.0. This introduces changes to the drop-in MLflow “scoring protocol” support, in the MLflow runtime for MLServer, to ensure it’s aligned with MLflow 2.0.  

MLServer is also shipped as a dependency of MLflow, therefore you can try it out today by installing MLflow as:

```bash
$ pip install mlflow[extras]
```

To learn more about how to use MLServer directly from the MLflow CLI, check out the [MLflow docs](https://www.mlflow.org/docs/latest/models.html#serving-with-mlserver).


### New Contributors
* [@johnpaulett](https://github.com/johnpaulett) made their first contribution in https://github.com/SeldonIO/MLServer/pull/633
* [@saeid93](https://github.com/saeid93) made their first contribution in https://github.com/SeldonIO/MLServer/pull/711
* [@RafalSkolasinski](https://github.com/RafalSkolasinski) made their first contribution in https://github.com/SeldonIO/MLServer/pull/720
* [@dumaas](https://github.com/dumaas) made their first contribution in https://github.com/SeldonIO/MLServer/pull/742
* [@Salehbigdeli](https://github.com/Salehbigdeli) made their first contribution in https://github.com/SeldonIO/MLServer/pull/776
* [@regen100](https://github.com/regen100) made their first contribution in https://github.com/SeldonIO/MLServer/pull/839

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.1.0...1.2.0

[Changes][1.2.0]


<a name="1.2.0.dev1"></a>
## [v1.2.0.dev1](https://github.com/SeldonIO/MLServer/releases/tag/1.2.0.dev1) - 01 Aug 2022



[Changes][1.2.0.dev1]


<a name="1.1.0"></a>
## [v1.1.0](https://github.com/SeldonIO/MLServer/releases/tag/1.1.0) - 01 Aug 2022



[Changes][1.1.0]


[1.3.5]: https://github.com/SeldonIO/MLServer/compare/1.3.4...1.3.5
[1.3.4]: https://github.com/SeldonIO/MLServer/compare/1.3.3...1.3.4
[1.3.3]: https://github.com/SeldonIO/MLServer/compare/1.3.2...1.3.3
[1.3.2]: https://github.com/SeldonIO/MLServer/compare/1.3.1...1.3.2
[1.3.1]: https://github.com/SeldonIO/MLServer/compare/1.3.0...1.3.1
[1.3.0]: https://github.com/SeldonIO/MLServer/compare/1.2.4...1.3.0
[1.2.4]: https://github.com/SeldonIO/MLServer/compare/1.2.3...1.2.4
[1.2.3]: https://github.com/SeldonIO/MLServer/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/SeldonIO/MLServer/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/SeldonIO/MLServer/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/SeldonIO/MLServer/compare/1.2.0.dev1...1.2.0
[1.2.0.dev1]: https://github.com/SeldonIO/MLServer/compare/1.1.0...1.2.0.dev1
[1.1.0]: https://github.com/SeldonIO/MLServer/tree/1.1.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.7.1 -->
