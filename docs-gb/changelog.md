---
hidden: true
---

# Changelog

## [1.6.0](https://github.com/SeldonIO/MLServer/releases/tag/1.6.0) - 26 Jun 2024

## Overview

### Upgrades

MLServer supports Pydantic V2.

### Features

MLServer supports streaming data to and from your models.

Streaming support is available for both the REST and gRPC servers:

* for the REST server is limited only to server streaming. This means that the client sends a single request to the server, and the server responds with a stream of data.
* for the gRPC server is available for both client and server streaming. This means that the client sends a stream of data to the server, and the server responds with a stream of data.

See our [docs](https://mlserver.readthedocs.io/en/1.6.0/user-guide/streaming.html) and [example](https://mlserver.readthedocs.io/en/1.6.0/examples/streaming/README.html) for more details.

## What's Changed

* fix(ci): fix typo in CI name by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1623
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1624
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1634
* Fix mlserver\_huggingface settings device type by [@geodavic](https://github.com/geodavic) in https://github.com/SeldonIO/MLServer/pull/1486
* fix: Adjust HF tests post-merge of PR [#1486](https://github.com/SeldonIO/MLServer/issues/1486) by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1635
* Update README.md w licensing clarification by [@paulb-seldon](https://github.com/paulb-seldon) in https://github.com/SeldonIO/MLServer/pull/1636
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1642
* fix(ci): optimise disk space for GH workers by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1644
* build: Update maintainers by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1659
* fix: Missing f-string directives by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1677
* build: Add Catboost runtime to Dependabot by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1689
* Fix JSON input shapes by [@ReveStobinson](https://github.com/ReveStobinson) in https://github.com/SeldonIO/MLServer/pull/1679
* build(deps): bump alibi-detect from 0.11.5 to 0.12.0 by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1702
* build(deps): bump alibi from 0.9.5 to 0.9.6 by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1704
* Docs correction - Updated README.md in mlflow to match column names order by [@vivekk0903](https://github.com/vivekk0903) in https://github.com/SeldonIO/MLServer/pull/1703
* fix(runtimes): Remove unused Pydantic dependencies by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1725
* test: Detect generate failures by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1729
* build: Add granularity in types generation by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1749
* Migrate to Pydantic v2 by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1748
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1753
* Revert "build(deps): bump uvicorn from 0.28.0 to 0.29.0" by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1758
* refactor(pydantic): Remaining migrations for deprecated functions by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1757
* Fixed openapi dataplane.yaml by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1752
* fix(pandas): Use Pydantic v2 compatible type by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1760
* Fix Pandas codec decoding from numpy arrays by [@lhnwrk](https://github.com/lhnwrk) in https://github.com/SeldonIO/MLServer/pull/1751
* build: Bump versions for Read the Docs by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1761
* docs: Remove quotes around local TOC by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1764
* Spawn worker in custom environment by [@lhnwrk](https://github.com/lhnwrk) in https://github.com/SeldonIO/MLServer/pull/1739
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1767
* basic contributing guide on contributing and opening a PR by [@bohemia420](https://github.com/bohemia420) in https://github.com/SeldonIO/MLServer/pull/1773
* Inference streaming support by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1750
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1779
* build: Lock GitHub runners' OS by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1765
* Removed text-model form benchmarking by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1790
* Bumped mlflow to 2.13.1 and gunicorn to 22.0.0 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1791
* Build(deps): Update to poetry version 1.8.3 in docker build by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1792
* Bumped werkzeug to 3.0.3 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1793
* Docs streaming by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1789
* Bump uvicorn 0.30.1 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1795
* Fixes for all-runtimes by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1794
* Fix BaseSettings import for pydantic v2 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1798
* Bumped preflight version to 1.9.7 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1797
* build: Install dependencies only in Tox environments by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1785
* Bumped to 1.6.0.dev2 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1803
* Fix CI/CD macos-huggingface by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1805
* Fixed macos kafka CI by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1807
* Update poetry lock by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1808
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1813
* Fix/macos all runtimes by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in https://github.com/SeldonIO/MLServer/pull/1823
* fix: Update stale reviewer in licenses.yml workflow by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1824
* ci: Merge changes from master to release branch by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1825

## New Contributors

* [@paulb-seldon](https://github.com/paulb-seldon) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1636
* [@ReveStobinson](https://github.com/ReveStobinson) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1679
* [@vivekk0903](https://github.com/vivekk0903) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1703
* [@RobertSamoilescu](https://github.com/RobertSamoilescu) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1752
* [@lhnwrk](https://github.com/lhnwrk) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1751
* [@bohemia420](https://github.com/bohemia420) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1773

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.5.0...1.6.0

[Changes](https://github.com/SeldonIO/MLServer/compare/1.5.0...1.6.0)

## [1.5.0](https://github.com/SeldonIO/MLServer/releases/tag/1.5.0) - 05 Mar 2024

## What's Changed

* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1592
* build: Migrate away from Node v16 actions by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1596
* build: Bump version and improve release doc by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1602
* build: Upgrade stale packages (fastapi, starlette, tensorflow, torch) by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1603
* fix(ci): tests and security workflow fixes by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1608
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1612
* fix(ci): Missing quote in CI test for all\_runtimes by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1617
* build(docker): Bump dependencies by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1618
* docs: List supported Python versions by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1591
* fix(ci): Have separate smaller tasks for release by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1619

## Notes

* We remove support for python 3.8, check https://github.com/SeldonIO/MLServer/pull/1603 for more info. Docker images for mlserver are already using python 3.10.

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.4.0...1.5.0

[Changes](https://github.com/SeldonIO/MLServer/compare/1.4.0...1.5.0)

## [1.4.0](https://github.com/SeldonIO/MLServer/releases/tag/1.4.0) - 28 Feb 2024

## What's Changed

* Free up some space for GH actions by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1282
* Introduce tracing with OpenTelemetry by [@vtaskow](https://github.com/vtaskow) in https://github.com/SeldonIO/MLServer/pull/1281
* Update release CI to use Poetry by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1283
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1284
* Add support for white-box explainers to alibi-explain runtime by [@ascillitoe](https://github.com/ascillitoe) in https://github.com/SeldonIO/MLServer/pull/1279
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1294
* Fix build-wheels.sh error when copying to output path by [@lc525](https://github.com/lc525) in https://github.com/SeldonIO/MLServer/pull/1286
* Fix typo by [@strickvl](https://github.com/strickvl) in https://github.com/SeldonIO/MLServer/pull/1289
* feat(logging): Distinguish logs from different models by [@vtaskow](https://github.com/vtaskow) in https://github.com/SeldonIO/MLServer/pull/1302
* Make sure we use our Response class by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1314
* Adding Quick-Start Guide to docs by [@ramonpzg](https://github.com/ramonpzg) in https://github.com/SeldonIO/MLServer/pull/1315
* feat(logging): Provide JSON-formatted structured logging as option by [@vtaskow](https://github.com/vtaskow) in https://github.com/SeldonIO/MLServer/pull/1308
* Bump in conda version and mamba solver by [@dtpryce](https://github.com/dtpryce) in https://github.com/SeldonIO/MLServer/pull/1298
* feat(huggingface): Merge model settings by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1337
* feat(huggingface): Load local artefacts in HuggingFace runtime by [@vtaskow](https://github.com/vtaskow) in https://github.com/SeldonIO/MLServer/pull/1319
* Document and test behaviour around NaN by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1346
* Address flakiness on 'mlserver build' tests by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1363
* Bump Poetry and lockfiles by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1369
* Bump Miniforge3 to 23.3.1 by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1372
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1373
* Improved huggingface batch logic by [@ajsalow](https://github.com/ajsalow) in https://github.com/SeldonIO/MLServer/pull/1336
* Add inference params support to MLFlow's custom invocation endpoint (… by [@M4nouel](https://github.com/M4nouel) in https://github.com/SeldonIO/MLServer/pull/1375
* Increase build space for runtime builds by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1385
* Fix minor typo in `sklearn` README by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in https://github.com/SeldonIO/MLServer/pull/1402
* Add catboost classifier support by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in https://github.com/SeldonIO/MLServer/pull/1403
* added model\_kwargs to huggingface model by [@nanbo-liu](https://github.com/nanbo-liu) in https://github.com/SeldonIO/MLServer/pull/1417
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in https://github.com/SeldonIO/MLServer/pull/1456
* Local response cache implementation by [@SachinVarghese](https://github.com/SachinVarghese) in https://github.com/SeldonIO/MLServer/pull/1440
* fix link to custom runtimes by [@kretes](https://github.com/kretes) in https://github.com/SeldonIO/MLServer/pull/1467
* Improve typing on `Environment` class by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in https://github.com/SeldonIO/MLServer/pull/1469
* build(dependabot): Change reviewers by [@jesse-c](https://github.com/jesse-c) in https://github.com/SeldonIO/MLServer/pull/1548
* MLServer changes from internal fork - deps and CI updates by [@sakoush](https://github.com/sakoush) in https://github.com/SeldonIO/MLServer/pull/1588

## New Contributors

* [@vtaskow](https://github.com/vtaskow) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1281
* [@lc525](https://github.com/lc525) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1286
* [@strickvl](https://github.com/strickvl) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1289
* [@ramonpzg](https://github.com/ramonpzg) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1315
* [@jesse-c](https://github.com/jesse-c) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1337
* [@ajsalow](https://github.com/ajsalow) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1336
* [@M4nouel](https://github.com/M4nouel) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1375
* [@nanbo-liu](https://github.com/nanbo-liu) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1417
* [@kretes](https://github.com/kretes) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1467

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.5...1.4.0

[Changes](https://github.com/SeldonIO/MLServer/compare/1.3.5...1.4.0)

## [1.3.5](https://github.com/SeldonIO/MLServer/releases/tag/1.3.5) - 10 Jul 2023

### What's Changed

* Rename HF codec to `hf` by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1268
* Publish is\_drift metric to Prom by [@joshsgoldstein](https://github.com/joshsgoldstein) in https://github.com/SeldonIO/MLServer/pull/1263

### New Contributors

* [@joshsgoldstein](https://github.com/joshsgoldstein) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1263

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.4...1.3.5

[Changes](https://github.com/SeldonIO/MLServer/compare/1.3.4...1.3.5)

## [1.3.4](https://github.com/SeldonIO/MLServer/releases/tag/1.3.4) - 21 Jun 2023

### What's Changed

* Silent logging by [@dtpryce](https://github.com/dtpryce) in https://github.com/SeldonIO/MLServer/pull/1230
* Fix `mlserver infer` with `BYTES` by [@RafalSkolasinski](https://github.com/RafalSkolasinski) in https://github.com/SeldonIO/MLServer/pull/1213

### New Contributors

* [@dtpryce](https://github.com/dtpryce) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1230

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.3...1.3.4

[Changes](https://github.com/SeldonIO/MLServer/compare/1.3.3...1.3.4)

## [1.3.3](https://github.com/SeldonIO/MLServer/releases/tag/1.3.3) - 05 Jun 2023

### What's Changed

* Add default LD\_LIBRARY\_PATH env var by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1120
* Adding cassava tutorial (mlserver + seldon core) by [@edshee](https://github.com/edshee) in https://github.com/SeldonIO/MLServer/pull/1156
* Add docs around converting to / from JSON by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1165
* Document SKLearn available outputs by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1167
* Fix minor typo in `alibi-explain` tests by [@ascillitoe](https://github.com/ascillitoe) in https://github.com/SeldonIO/MLServer/pull/1170
* Add support for `.ubj` models and improve XGBoost docs by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1168
* Fix content type annotations for pandas codecs by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1162
* Added option to configure the grpc histogram by [@cristiancl25](https://github.com/cristiancl25) in https://github.com/SeldonIO/MLServer/pull/1143
* Add OS classifiers to project's metadata by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1171
* Don't use `qsize` for parallel worker queue by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1169
* Fix small typo in Python API docs by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in https://github.com/SeldonIO/MLServer/pull/1174
* Fix star import in `mlserver.codecs.*` by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1172

### New Contributors

* [@cristiancl25](https://github.com/cristiancl25) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1143
* [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1174

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.2...1.3.3

[Changes](https://github.com/SeldonIO/MLServer/compare/1.3.2...1.3.3)

## [1.3.2](https://github.com/SeldonIO/MLServer/releases/tag/1.3.2) - 10 May 2023

### What's Changed

* Use default initialiser if not using a custom env by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1104
* Add support for online drift detectors by [@ascillitoe](https://github.com/ascillitoe) in https://github.com/SeldonIO/MLServer/pull/1108
* added intera and inter op parallelism parameters to the hugggingface … by [@saeid93](https://github.com/saeid93) in https://github.com/SeldonIO/MLServer/pull/1081
* Fix settings reference in runtime docs by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1109
* Bump Alibi libs requirements by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1121
* Add default LD\_LIBRARY\_PATH env var by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1120
* Ignore both .metrics and .envs folders by [@adriangonz](https://github.com/adriangonz) in https://github.com/SeldonIO/MLServer/pull/1132

### New Contributors

* [@ascillitoe](https://github.com/ascillitoe) made their first contribution in https://github.com/SeldonIO/MLServer/pull/1108

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.1...1.3.2

[Changes](https://github.com/SeldonIO/MLServer/compare/1.3.1...1.3.2)

## [1.3.1](https://github.com/SeldonIO/MLServer/releases/tag/1.3.1) - 27 Apr 2023

### What's Changed

* Move OpenAPI schemas into Python package ([#1095](https://github.com/SeldonIO/MLServer/issues/1095))

[Changes](https://github.com/SeldonIO/MLServer/compare/1.3.0...1.3.1)

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

* `[mlserver.register()](https://mlserver.readthedocs.io/en/latest/reference/api/metrics.html#mlserver.register)`: Register a new metric.
* `[mlserver.log()](https://mlserver.readthedocs.io/en/latest/reference/api/metrics.html#mlserver.log)`: Log a new set of metric / value pairs.

Custom metrics will generally be registered in the `[load()](https://mlserver.readthedocs.io/en/latest/reference/api/model.html#mlserver.MLModel.load)` method and then used in the `[predict()](https://mlserver.readthedocs.io/en/latest/reference/api/model.html#mlserver.MLModel.predict)` method of your [custom runtime](https://mlserver.readthedocs.io/en/latest/user-guide/custom.html). These metrics can then be polled and queried via [Prometheus](https://mlserver.readthedocs.io/en/latest/user-guide/metrics.html#settings).

![image](https://user-images.githubusercontent.com/1577620/234798211-9e538439-4914-4aa6-9c3f-539a66e3ce54.png)

#### OpenAPI

MLServer `1.3.0` now includes an autogenerated Swagger UI which can be used to interact dynamically with the Open Inference Protocol.

The autogenerated Swagger UI can be accessed under the `/v2/docs` endpoint.

![https://mlserver.readthedocs.io/en/latest/\_images/swagger-ui.png](https://mlserver.readthedocs.io/en/latest/_images/swagger-ui.png)

Alongside the [general API documentation](https://mlserver.readthedocs.io/en/latest/user-guide/openapi.html#Swagger-UI), MLServer also exposes now a set of API docs tailored to individual models, showing the specific endpoints available for each one.

The model-specific autogenerated Swagger UI can be accessed under the following endpoints:

* `/v2/models/{model_name}/docs`
* `/v2/models/{model_name}/versions/{model_version}/docs`

#### HuggingFace Improvements

MLServer now includes improved Codec support for all the main different types that can be returned by HugginFace models - ensuring that the values returned via the Open Inference Protocol are more semantic and meaningful.

Massive thanks to [@pepesi](https://github.com/pepesi) for taking the lead on improving the HuggingFace runtime!

#### Support for Custom Model Repositories

Internally, MLServer leverages a Model Repository implementation which is used to discover and find different models (and their versions) available to load. The latest version of MLServer will now allow you to swap this for your own model repository implementation - letting you integrate against your own model repository workflows.

This is exposed via the [model\_repository\_implementation](https://mlserver.readthedocs.io/en/latest/reference/settings.html#mlserver.settings.Settings.model_repository_implementation) flag of your `settings.json` configuration file.

Thanks to [@jgallardorama](https://github.com/jgallardorama) (aka [@jgallardorama-itx](https://github.com/jgallardorama-itx) ) for his effort contributing this feature!

#### Batch and Worker Queue Metrics

MLServer `1.3.0` introduces a [new set of metrics](https://mlserver.readthedocs.io/en/latest/user-guide/metrics.html#default-metrics) to increase visibility around two of its internal queues:

* [Adaptive batching](https://mlserver.readthedocs.io/en/latest/user-guide/adaptive-batching.html) queue: used to accumulate request batches on the fly.
* [Parallel inference](https://mlserver.readthedocs.io/en/latest/user-guide/parallel-inference.html) queue: used to send over requests to the inference worker pool.

Many thanks to [@alvarorsant](https://github.com/alvarorsant) for taking the time to implement this highly requested feature!

#### Image Size Optimisations

The latest version of MLServer includes a few optimisations around image size, which help reduce the size of the official set of images by more than \~60% - making them more convenient to use and integrate within your workloads. In the case of the full `seldonio/mlserver:1.3.0` image (including all runtimes and dependencies), this means going from 10GB down to \~3GB.

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

[Changes](https://github.com/SeldonIO/MLServer/compare/1.2.4...1.3.0)

## [1.2.4](https://github.com/SeldonIO/MLServer/releases/tag/1.2.4) - 10 Mar 2023

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.3...1.2.4

[Changes](https://github.com/SeldonIO/MLServer/compare/1.2.3...1.2.4)

## [1.2.3](https://github.com/SeldonIO/MLServer/releases/tag/1.2.3) - 16 Jan 2023

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.2...1.2.3

[Changes](https://github.com/SeldonIO/MLServer/compare/1.2.2...1.2.3)

## [1.2.2](https://github.com/SeldonIO/MLServer/releases/tag/1.2.2) - 16 Jan 2023

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.1...1.2.2

[Changes](https://github.com/SeldonIO/MLServer/compare/1.2.1...1.2.2)

## [1.2.1](https://github.com/SeldonIO/MLServer/releases/tag/1.2.1) - 19 Dec 2022

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.0...1.2.1

[Changes](https://github.com/SeldonIO/MLServer/compare/1.2.0...1.2.1)

## [1.2.0](https://github.com/SeldonIO/MLServer/releases/tag/1.2.0) - 25 Nov 2022

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

* The main MLServer process won’t load an extra replica of the model anymore. Instead, all computing will occur on the parallel inference pool.
* The worker pool will now ensure that all requests are executed on each worker’s AsyncIO loop, thus optimising compute time vs IO time.
* Several improvements around logging from the inference workers.

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

[Changes](https://github.com/SeldonIO/MLServer/compare/1.2.0.dev1...1.2.0)

## [v1.2.0.dev1](https://github.com/SeldonIO/MLServer/releases/tag/1.2.0.dev1) - 01 Aug 2022

[Changes](https://github.com/SeldonIO/MLServer/compare/1.1.0...1.2.0.dev1)

## [v1.1.0](https://github.com/SeldonIO/MLServer/releases/tag/1.1.0) - 01 Aug 2022

[Changes](https://github.com/SeldonIO/MLServer/tree/1.1.0)
