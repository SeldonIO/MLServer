# Changelog


<a id="1.7.1"></a>
## [1.7.1](https://github.com/SeldonIO/MLServer/releases/tag/1.7.1) - 2025-06-06

<!-- Release notes generated using configuration in .github/release.yml at 1.7.1 -->

## Fixes
* Set a lower bound for `mlflow` in `mlserver-mlflow` by [@crispin-ki](https://github.com/crispin-ki) in [#2114](https://github.com/SeldonIO/MLServer/pull/2114)
* Set lower bounds for `protobuf`, `grpcio`, and `grpcio-tools` by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2175](https://github.com/SeldonIO/MLServer/pull/2175)
* Added support for bytes encoding in `PandasCodec` by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2117](https://github.com/SeldonIO/MLServer/pull/2117)

## What's Changed
* Included more docker labels by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2106](https://github.com/SeldonIO/MLServer/pull/2106)
* Fix too loose mlflow dependency constraint in mlserver-mlflow by [@crispin-ki](https://github.com/crispin-ki) in [#2114](https://github.com/SeldonIO/MLServer/pull/2114)
* Fixed byte encoding in the PandasCodec by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2117](https://github.com/SeldonIO/MLServer/pull/2117)
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in [#2108](https://github.com/SeldonIO/MLServer/pull/2108)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#2174](https://github.com/SeldonIO/MLServer/pull/2174)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#2176](https://github.com/SeldonIO/MLServer/pull/2176)
* Fix protobuf bounds by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2175](https://github.com/SeldonIO/MLServer/pull/2175)
* Revert "build(deps-dev): bump transformers from 4.41.2 to 4.52.4 ([#2170](https://github.com/SeldonIO/MLServer/issues/2170))" by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2177](https://github.com/SeldonIO/MLServer/pull/2177)
* ci: Merge change for release 1.7.1 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2178](https://github.com/SeldonIO/MLServer/pull/2178)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#2180](https://github.com/SeldonIO/MLServer/pull/2180)
* ci: Merge change for release 1.7.1 [2]  ([#2180](https://github.com/SeldonIO/MLServer/issues/2180)) by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2182](https://github.com/SeldonIO/MLServer/pull/2182)

## New Contributors
* [@crispin-ki](https://github.com/crispin-ki) made their first contribution in [#2114](https://github.com/SeldonIO/MLServer/pull/2114)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.7.0...1.7.1

[Changes][1.7.1]


<a id="1.7.0"></a>
## [1.7.0](https://github.com/SeldonIO/MLServer/releases/tag/1.7.0) - 2025-04-11

<!-- Release notes generated using configuration in .github/release.yml at 1.7.0 -->

## Overview

### Features
* MLServer has now support for Python 3.11 and 3.12 by [@shivakrishnaah](https://github.com/shivakrishnaah) in ([#1951](https://github.com/SeldonIO/MLServer/issues/1951))
* MLServer now supports enabling assignment of models to dedicated inference pool groups to avoid risk of starvation by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in (#[#2040](https://github.com/SeldonIO/MLServer/issues/2040))
* MLServer now includes compatibility with additional column types available in the MLflow runtime such as: [Array](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.types.html#mlflow.types.schema.Array), [Map](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.types.html#mlflow.types.schema.Map), [Object](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.types.html#mlflow.types.schema.Object), [Any](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.types.html#mlflow.types.schema.Map) by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in ([#2080](https://github.com/SeldonIO/MLServer/issues/2080))

### Fixes
* Relaxing Pydantic dependencies by [@lemonhead94](https://github.com/lemonhead94) in ([#1928](https://github.com/SeldonIO/MLServer/issues/1928))
* Adjusted the version range for FastAPI  to ensure compatibility with future releases by [@sergioave](https://github.com/sergioave)  in ([#1954](https://github.com/SeldonIO/MLServer/issues/1954))
* Forward rest parameters to model [@idlefella](https://github.com/idlefella) in ([#1921](https://github.com/SeldonIO/MLServer/issues/1921))
* Force clean up env fix by [@sakoush](https://github.com/sakoush) in ([#2029](https://github.com/SeldonIO/MLServer/issues/2029))
* PandasCodec improperly encoding columns of numeric lists fix by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in ([#2080](https://github.com/SeldonIO/MLServer/issues/2080))
* Opentelemetry dependency mismatch fix by [@lawrence-c](https://github.com/lawrence-c) in ([#2088](https://github.com/SeldonIO/MLServer/issues/2088))
* AdaptiveBatcher timeout calculation fix by [@hanlaur](https://github.com/hanlaur) in ([#2093](https://github.com/SeldonIO/MLServer/issues/2093))

## What's Changed
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in [#1905](https://github.com/SeldonIO/MLServer/pull/1905)
* docs: add docs for gitbook by [@sakoush](https://github.com/sakoush) in [#1919](https://github.com/SeldonIO/MLServer/pull/1919)
* Relaxing Pydantic dependencies by [@lemonhead94](https://github.com/lemonhead94) in [#1928](https://github.com/SeldonIO/MLServer/pull/1928)
* build(deps): Upgrade fastapi and starlette by [@sakoush](https://github.com/sakoush) in [#1934](https://github.com/SeldonIO/MLServer/pull/1934)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1935](https://github.com/SeldonIO/MLServer/pull/1935)
* Update FastAPI version constraint by [@sergioave](https://github.com/sergioave) in [#1954](https://github.com/SeldonIO/MLServer/pull/1954)
* Forward rest parameters to model by [@idlefella](https://github.com/idlefella) in [#1921](https://github.com/SeldonIO/MLServer/pull/1921)
* Revert "build(deps): bump mlflow from 2.18.0 to 2.19.0 in /runtimes/mlflow" by [@sakoush](https://github.com/sakoush) in [#1988](https://github.com/SeldonIO/MLServer/pull/1988)
* Added dependency upgrades for python3.12 support by [@shivakrishnaah](https://github.com/shivakrishnaah) in [#1951](https://github.com/SeldonIO/MLServer/pull/1951)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1991](https://github.com/SeldonIO/MLServer/pull/1991)
* Further CI fixes for py312 support by [@sakoush](https://github.com/sakoush) in [#1992](https://github.com/SeldonIO/MLServer/pull/1992)
* Revert "build(deps): bump python-multipart from 0.0.9 to 0.0.18 in /runtimes/alibi-detect" by [@sakoush](https://github.com/sakoush) in [#1994](https://github.com/SeldonIO/MLServer/pull/1994)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#2027](https://github.com/SeldonIO/MLServer/pull/2027)
* Force clean up env (for py 3.12) by [@sakoush](https://github.com/sakoush) in [#2029](https://github.com/SeldonIO/MLServer/pull/2029)
* Pinned preflight to latest version by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2041](https://github.com/SeldonIO/MLServer/pull/2041)
* Bump gevent to 24.11.1 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2042](https://github.com/SeldonIO/MLServer/pull/2042)
* Bumped python-multipart to 0.0.20 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2043](https://github.com/SeldonIO/MLServer/pull/2043)
* Bumped python-multipart-0.0.20 on alibi-explain runtime by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2044](https://github.com/SeldonIO/MLServer/pull/2044)
* Included separate inference pool by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2040](https://github.com/SeldonIO/MLServer/pull/2040)
* Wrote docs for inference_pool_gid by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2045](https://github.com/SeldonIO/MLServer/pull/2045)
* Update lightgbm in alibi runtime to 4.6 by [@sakoush](https://github.com/sakoush) in [#2081](https://github.com/SeldonIO/MLServer/pull/2081)
* Fix pandas codec by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2080](https://github.com/SeldonIO/MLServer/pull/2080)
* Fix interceptors insert tuple -> list by [@lawrence-c](https://github.com/lawrence-c) in [#2088](https://github.com/SeldonIO/MLServer/pull/2088)
* Fix AdaptiveBatcher timeout calculation by [@hanlaur](https://github.com/hanlaur) in [#2093](https://github.com/SeldonIO/MLServer/pull/2093)
* Fix onnxruntime version by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2100](https://github.com/SeldonIO/MLServer/pull/2100)
* Included labels for preflight checks by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2101](https://github.com/SeldonIO/MLServer/pull/2101)
* Bumped poetry to 2.1.1 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2103](https://github.com/SeldonIO/MLServer/pull/2103)
* Add installation for poetry export plugin by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2104](https://github.com/SeldonIO/MLServer/pull/2104)
* ci: Merge change for release 1.7.0 [4] by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#2107](https://github.com/SeldonIO/MLServer/pull/2107)

## New Contributors
* [@lemonhead94](https://github.com/lemonhead94) made their first contribution in [#1928](https://github.com/SeldonIO/MLServer/pull/1928)
* [@sergioave](https://github.com/sergioave) made their first contribution in [#1954](https://github.com/SeldonIO/MLServer/pull/1954)
* [@shivakrishnaah](https://github.com/shivakrishnaah) made their first contribution in [#1951](https://github.com/SeldonIO/MLServer/pull/1951)
* [@lawrence-c](https://github.com/lawrence-c) made their first contribution in [#2088](https://github.com/SeldonIO/MLServer/pull/2088)
* [@hanlaur](https://github.com/hanlaur) made their first contribution in [#2093](https://github.com/SeldonIO/MLServer/pull/2093)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.6.1...1.7.0

[Changes][1.7.0]


<a id="1.6.1"></a>
## [1.6.1](https://github.com/SeldonIO/MLServer/releases/tag/1.6.1) - 2024-09-10

<!-- Release notes generated using configuration in .github/release.yml at 1.6.1 -->

## Overview

### Features
MLServer now offers an option to use pre-existing Python environments by specifying a path to the environment to be used - by [@idlefella](https://github.com/idlefella) in ([#1891](https://github.com/SeldonIO/MLServer/issues/1891))

### Releases
MLServer released catboost runtime which allows serving [catboost](https://catboost.ai/) models with MLServer - by [@sakoush](https://github.com/sakoush) in ([#1839](https://github.com/SeldonIO/MLServer/issues/1839))

### Fixes
* Kafka json byte encoding fix to match rest server by [@DerTiedemann](https://github.com/DerTiedemann) and [@sakoush](https://github.com/sakoush) in ([#1622](https://github.com/SeldonIO/MLServer/issues/1622))
* Prometheus interceptor fix for gRPC streaming by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in ([#1858](https://github.com/SeldonIO/MLServer/issues/1858))


## What's Changed
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1812](https://github.com/SeldonIO/MLServer/pull/1812)
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in [#1830](https://github.com/SeldonIO/MLServer/pull/1830)
* Update release.yml to include catboost by [@sakoush](https://github.com/sakoush) in [#1839](https://github.com/SeldonIO/MLServer/pull/1839)
* Fix kafka json byte encoding to match rest server by [@DerTiedemann](https://github.com/DerTiedemann) in [#1622](https://github.com/SeldonIO/MLServer/pull/1622)
* Included Prometheus interceptor support for gRPC streaming by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1858](https://github.com/SeldonIO/MLServer/pull/1858)
* Run gRPC test serially by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1872](https://github.com/SeldonIO/MLServer/pull/1872)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1886](https://github.com/SeldonIO/MLServer/pull/1886)
* Feature/support existing environments by [@idlefella](https://github.com/idlefella) in [#1891](https://github.com/SeldonIO/MLServer/pull/1891)
* Fix tensorflow upperbound macos by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1901](https://github.com/SeldonIO/MLServer/pull/1901)
* ci: Merge change for release 1.6.1  by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1902](https://github.com/SeldonIO/MLServer/pull/1902)
* Bump preflight to 1.10.0 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1903](https://github.com/SeldonIO/MLServer/pull/1903)
* ci: Merge change for release 1.6.1 [2] by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1904](https://github.com/SeldonIO/MLServer/pull/1904)

## New Contributors
* [@DerTiedemann](https://github.com/DerTiedemann) made their first contribution in [#1622](https://github.com/SeldonIO/MLServer/pull/1622)
* [@idlefella](https://github.com/idlefella) made their first contribution in [#1891](https://github.com/SeldonIO/MLServer/pull/1891)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.6.0...1.6.1

[Changes][1.6.1]


<a id="1.6.0"></a>
## [1.6.0](https://github.com/SeldonIO/MLServer/releases/tag/1.6.0) - 2024-06-26

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
* fix(ci): fix typo in CI name by [@sakoush](https://github.com/sakoush) in [#1623](https://github.com/SeldonIO/MLServer/pull/1623)
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in [#1624](https://github.com/SeldonIO/MLServer/pull/1624)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1634](https://github.com/SeldonIO/MLServer/pull/1634)
* Fix mlserver_huggingface settings device type by [@geodavic](https://github.com/geodavic) in [#1486](https://github.com/SeldonIO/MLServer/pull/1486)
* fix: Adjust HF tests post-merge of PR [#1486](https://github.com/SeldonIO/MLServer/issues/1486) by [@sakoush](https://github.com/sakoush) in [#1635](https://github.com/SeldonIO/MLServer/pull/1635)
* Update README.md w licensing clarification by [@paulb-seldon](https://github.com/paulb-seldon) in [#1636](https://github.com/SeldonIO/MLServer/pull/1636)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1642](https://github.com/SeldonIO/MLServer/pull/1642)
* fix(ci): optimise disk space for GH workers by [@sakoush](https://github.com/sakoush) in [#1644](https://github.com/SeldonIO/MLServer/pull/1644)
* build: Update maintainers by [@jesse-c](https://github.com/jesse-c) in [#1659](https://github.com/SeldonIO/MLServer/pull/1659)
* fix: Missing f-string directives by [@jesse-c](https://github.com/jesse-c) in [#1677](https://github.com/SeldonIO/MLServer/pull/1677)
* build: Add Catboost runtime to Dependabot by [@jesse-c](https://github.com/jesse-c) in [#1689](https://github.com/SeldonIO/MLServer/pull/1689)
* Fix JSON input shapes by [@ReveStobinson](https://github.com/ReveStobinson) in [#1679](https://github.com/SeldonIO/MLServer/pull/1679)
* build(deps): bump alibi-detect from 0.11.5 to 0.12.0 by [@jesse-c](https://github.com/jesse-c) in [#1702](https://github.com/SeldonIO/MLServer/pull/1702)
* build(deps): bump alibi from 0.9.5 to 0.9.6 by [@jesse-c](https://github.com/jesse-c) in [#1704](https://github.com/SeldonIO/MLServer/pull/1704)
* Docs correction - Updated README.md in mlflow to match column names order by [@vivekk0903](https://github.com/vivekk0903) in [#1703](https://github.com/SeldonIO/MLServer/pull/1703)
* fix(runtimes): Remove unused Pydantic dependencies by [@jesse-c](https://github.com/jesse-c) in [#1725](https://github.com/SeldonIO/MLServer/pull/1725)
* test: Detect generate failures by [@jesse-c](https://github.com/jesse-c) in [#1729](https://github.com/SeldonIO/MLServer/pull/1729)
* build: Add granularity in types generation by [@jesse-c](https://github.com/jesse-c) in [#1749](https://github.com/SeldonIO/MLServer/pull/1749)
* Migrate to Pydantic v2 by [@jesse-c](https://github.com/jesse-c) in [#1748](https://github.com/SeldonIO/MLServer/pull/1748)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1753](https://github.com/SeldonIO/MLServer/pull/1753)
* Revert "build(deps): bump uvicorn from 0.28.0 to 0.29.0" by [@jesse-c](https://github.com/jesse-c) in [#1758](https://github.com/SeldonIO/MLServer/pull/1758)
* refactor(pydantic): Remaining migrations for deprecated functions by [@jesse-c](https://github.com/jesse-c) in [#1757](https://github.com/SeldonIO/MLServer/pull/1757)
* Fixed openapi dataplane.yaml by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1752](https://github.com/SeldonIO/MLServer/pull/1752)
* fix(pandas): Use Pydantic v2 compatible type by [@jesse-c](https://github.com/jesse-c) in [#1760](https://github.com/SeldonIO/MLServer/pull/1760)
* Fix Pandas codec decoding from numpy arrays by [@lhnwrk](https://github.com/lhnwrk) in [#1751](https://github.com/SeldonIO/MLServer/pull/1751)
* build: Bump versions for Read the Docs by [@jesse-c](https://github.com/jesse-c) in [#1761](https://github.com/SeldonIO/MLServer/pull/1761)
* docs: Remove quotes around local TOC by [@jesse-c](https://github.com/jesse-c) in [#1764](https://github.com/SeldonIO/MLServer/pull/1764)
* Spawn worker in custom environment by [@lhnwrk](https://github.com/lhnwrk) in [#1739](https://github.com/SeldonIO/MLServer/pull/1739)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1767](https://github.com/SeldonIO/MLServer/pull/1767)
* basic contributing guide on contributing and opening a PR by [@bohemia420](https://github.com/bohemia420) in [#1773](https://github.com/SeldonIO/MLServer/pull/1773)
* Inference streaming support by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1750](https://github.com/SeldonIO/MLServer/pull/1750)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1779](https://github.com/SeldonIO/MLServer/pull/1779)
* build: Lock GitHub runners' OS by [@jesse-c](https://github.com/jesse-c) in [#1765](https://github.com/SeldonIO/MLServer/pull/1765)
* Removed text-model form benchmarking by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1790](https://github.com/SeldonIO/MLServer/pull/1790)
* Bumped mlflow to 2.13.1 and gunicorn to 22.0.0 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1791](https://github.com/SeldonIO/MLServer/pull/1791)
* Build(deps): Update to poetry version 1.8.3 in docker build by [@sakoush](https://github.com/sakoush) in [#1792](https://github.com/SeldonIO/MLServer/pull/1792)
* Bumped werkzeug to 3.0.3 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1793](https://github.com/SeldonIO/MLServer/pull/1793)
* Docs streaming by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1789](https://github.com/SeldonIO/MLServer/pull/1789)
* Bump uvicorn 0.30.1 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1795](https://github.com/SeldonIO/MLServer/pull/1795)
* Fixes for all-runtimes by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1794](https://github.com/SeldonIO/MLServer/pull/1794)
* Fix BaseSettings import for pydantic v2 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1798](https://github.com/SeldonIO/MLServer/pull/1798)
* Bumped preflight version to 1.9.7 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1797](https://github.com/SeldonIO/MLServer/pull/1797)
* build: Install dependencies only in Tox environments  by [@jesse-c](https://github.com/jesse-c) in [#1785](https://github.com/SeldonIO/MLServer/pull/1785)
* Bumped to 1.6.0.dev2 by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1803](https://github.com/SeldonIO/MLServer/pull/1803)
* Fix CI/CD macos-huggingface by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1805](https://github.com/SeldonIO/MLServer/pull/1805)
* Fixed macos kafka CI by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1807](https://github.com/SeldonIO/MLServer/pull/1807)
* Update poetry lock by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1808](https://github.com/SeldonIO/MLServer/pull/1808)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1813](https://github.com/SeldonIO/MLServer/pull/1813)
* Fix/macos all runtimes by [@RobertSamoilescu](https://github.com/RobertSamoilescu) in [#1823](https://github.com/SeldonIO/MLServer/pull/1823)
* fix: Update stale reviewer in licenses.yml workflow by [@sakoush](https://github.com/sakoush) in [#1824](https://github.com/SeldonIO/MLServer/pull/1824)
* ci: Merge changes from master to release branch by [@sakoush](https://github.com/sakoush) in [#1825](https://github.com/SeldonIO/MLServer/pull/1825)

## New Contributors
* [@paulb-seldon](https://github.com/paulb-seldon) made their first contribution in [#1636](https://github.com/SeldonIO/MLServer/pull/1636)
* [@ReveStobinson](https://github.com/ReveStobinson) made their first contribution in [#1679](https://github.com/SeldonIO/MLServer/pull/1679)
* [@vivekk0903](https://github.com/vivekk0903) made their first contribution in [#1703](https://github.com/SeldonIO/MLServer/pull/1703)
* [@RobertSamoilescu](https://github.com/RobertSamoilescu) made their first contribution in [#1752](https://github.com/SeldonIO/MLServer/pull/1752)
* [@lhnwrk](https://github.com/lhnwrk) made their first contribution in [#1751](https://github.com/SeldonIO/MLServer/pull/1751)
* [@bohemia420](https://github.com/bohemia420) made their first contribution in [#1773](https://github.com/SeldonIO/MLServer/pull/1773)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.5.0...1.6.0

[Changes][1.6.0]


<a id="1.5.0"></a>
## [1.5.0](https://github.com/SeldonIO/MLServer/releases/tag/1.5.0) - 2024-03-05

## What's Changed

* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in [#1592](https://github.com/SeldonIO/MLServer/pull/1592)
* build: Migrate away from Node v16 actions by [@jesse-c](https://github.com/jesse-c) in [#1596](https://github.com/SeldonIO/MLServer/pull/1596)
* build: Bump version and improve release doc by [@jesse-c](https://github.com/jesse-c) in [#1602](https://github.com/SeldonIO/MLServer/pull/1602)
* build: Upgrade stale packages (fastapi, starlette, tensorflow, torch) by [@sakoush](https://github.com/sakoush) in [#1603](https://github.com/SeldonIO/MLServer/pull/1603)
* fix(ci): tests and security workflow fixes by [@sakoush](https://github.com/sakoush) in [#1608](https://github.com/SeldonIO/MLServer/pull/1608)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1612](https://github.com/SeldonIO/MLServer/pull/1612)
* fix(ci): Missing quote in CI test for all_runtimes by [@sakoush](https://github.com/sakoush) in [#1617](https://github.com/SeldonIO/MLServer/pull/1617)
* build(docker): Bump dependencies by [@jesse-c](https://github.com/jesse-c) in [#1618](https://github.com/SeldonIO/MLServer/pull/1618)
* docs: List supported Python versions  by [@jesse-c](https://github.com/jesse-c) in [#1591](https://github.com/SeldonIO/MLServer/pull/1591)
* fix(ci): Have separate smaller tasks for release by [@sakoush](https://github.com/sakoush) in [#1619](https://github.com/SeldonIO/MLServer/pull/1619)


## Notes
* We remove support for python 3.8, check [#1603](https://github.com/SeldonIO/MLServer/pull/1603) for more info. Docker images for mlserver are already using python 3.10.

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.4.0...1.5.0

[Changes][1.5.0]


<a id="1.4.0"></a>
## [1.4.0](https://github.com/SeldonIO/MLServer/releases/tag/1.4.0) - 2024-02-28

<!-- Release notes generated using configuration in .github/release.yml at 1.4.0 -->

## What's Changed
* Free up some space for GH actions by [@adriangonz](https://github.com/adriangonz) in [#1282](https://github.com/SeldonIO/MLServer/pull/1282)
* Introduce tracing with OpenTelemetry by [@vtaskow](https://github.com/vtaskow) in [#1281](https://github.com/SeldonIO/MLServer/pull/1281)
* Update release CI to use Poetry by [@adriangonz](https://github.com/adriangonz) in [#1283](https://github.com/SeldonIO/MLServer/pull/1283)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1284](https://github.com/SeldonIO/MLServer/pull/1284)
* Add support for white-box explainers to alibi-explain runtime by [@ascillitoe](https://github.com/ascillitoe) in [#1279](https://github.com/SeldonIO/MLServer/pull/1279)
* Update CHANGELOG by [@github-actions](https://github.com/github-actions) in [#1294](https://github.com/SeldonIO/MLServer/pull/1294)
* Fix build-wheels.sh error when copying to output path by [@lc525](https://github.com/lc525) in [#1286](https://github.com/SeldonIO/MLServer/pull/1286)
* Fix typo by [@strickvl](https://github.com/strickvl) in [#1289](https://github.com/SeldonIO/MLServer/pull/1289)
* feat(logging): Distinguish logs from different models by [@vtaskow](https://github.com/vtaskow) in [#1302](https://github.com/SeldonIO/MLServer/pull/1302)
* Make sure we use our Response class by [@adriangonz](https://github.com/adriangonz) in [#1314](https://github.com/SeldonIO/MLServer/pull/1314)
* Adding Quick-Start Guide to docs by [@ramonpzg](https://github.com/ramonpzg) in [#1315](https://github.com/SeldonIO/MLServer/pull/1315)
* feat(logging): Provide JSON-formatted structured logging as option by [@vtaskow](https://github.com/vtaskow) in [#1308](https://github.com/SeldonIO/MLServer/pull/1308)
* Bump in conda version and mamba solver  by [@dtpryce](https://github.com/dtpryce) in [#1298](https://github.com/SeldonIO/MLServer/pull/1298)
* feat(huggingface): Merge model settings by [@jesse-c](https://github.com/jesse-c) in [#1337](https://github.com/SeldonIO/MLServer/pull/1337)
* feat(huggingface): Load local artefacts in HuggingFace runtime by [@vtaskow](https://github.com/vtaskow) in [#1319](https://github.com/SeldonIO/MLServer/pull/1319)
* Document and test behaviour around NaN by [@adriangonz](https://github.com/adriangonz) in [#1346](https://github.com/SeldonIO/MLServer/pull/1346)
* Address flakiness on 'mlserver build' tests by [@adriangonz](https://github.com/adriangonz) in [#1363](https://github.com/SeldonIO/MLServer/pull/1363)
* Bump Poetry and lockfiles by [@adriangonz](https://github.com/adriangonz) in [#1369](https://github.com/SeldonIO/MLServer/pull/1369)
* Bump Miniforge3 to 23.3.1 by [@adriangonz](https://github.com/adriangonz) in [#1372](https://github.com/SeldonIO/MLServer/pull/1372)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1373](https://github.com/SeldonIO/MLServer/pull/1373)
* Improved huggingface batch logic by [@ajsalow](https://github.com/ajsalow) in [#1336](https://github.com/SeldonIO/MLServer/pull/1336)
* Add inference params support to MLFlow's custom invocation endpoint (… by [@M4nouel](https://github.com/M4nouel) in [#1375](https://github.com/SeldonIO/MLServer/pull/1375)
* Increase build space for runtime builds by [@adriangonz](https://github.com/adriangonz) in [#1385](https://github.com/SeldonIO/MLServer/pull/1385)
* Fix minor typo in `sklearn` README by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in [#1402](https://github.com/SeldonIO/MLServer/pull/1402)
* Add catboost classifier support by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in [#1403](https://github.com/SeldonIO/MLServer/pull/1403)
* added model_kwargs to huggingface model by [@nanbo-liu](https://github.com/nanbo-liu) in [#1417](https://github.com/SeldonIO/MLServer/pull/1417)
* Re-generate License Info by [@github-actions](https://github.com/github-actions) in [#1456](https://github.com/SeldonIO/MLServer/pull/1456)
* Local response cache implementation by [@SachinVarghese](https://github.com/SachinVarghese) in [#1440](https://github.com/SeldonIO/MLServer/pull/1440)
* fix link to custom runtimes by [@kretes](https://github.com/kretes) in [#1467](https://github.com/SeldonIO/MLServer/pull/1467)
* Improve typing on `Environment` class by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) in [#1469](https://github.com/SeldonIO/MLServer/pull/1469)
* build(dependabot): Change reviewers by [@jesse-c](https://github.com/jesse-c) in [#1548](https://github.com/SeldonIO/MLServer/pull/1548)
* MLServer changes from internal fork - deps and CI updates by [@sakoush](https://github.com/sakoush) in [#1588](https://github.com/SeldonIO/MLServer/pull/1588)

## New Contributors
* [@vtaskow](https://github.com/vtaskow) made their first contribution in [#1281](https://github.com/SeldonIO/MLServer/pull/1281)
* [@lc525](https://github.com/lc525) made their first contribution in [#1286](https://github.com/SeldonIO/MLServer/pull/1286)
* [@strickvl](https://github.com/strickvl) made their first contribution in [#1289](https://github.com/SeldonIO/MLServer/pull/1289)
* [@ramonpzg](https://github.com/ramonpzg) made their first contribution in [#1315](https://github.com/SeldonIO/MLServer/pull/1315)
* [@jesse-c](https://github.com/jesse-c) made their first contribution in [#1337](https://github.com/SeldonIO/MLServer/pull/1337)
* [@ajsalow](https://github.com/ajsalow) made their first contribution in [#1336](https://github.com/SeldonIO/MLServer/pull/1336)
* [@M4nouel](https://github.com/M4nouel) made their first contribution in [#1375](https://github.com/SeldonIO/MLServer/pull/1375)
* [@nanbo-liu](https://github.com/nanbo-liu) made their first contribution in [#1417](https://github.com/SeldonIO/MLServer/pull/1417)
* [@kretes](https://github.com/kretes) made their first contribution in [#1467](https://github.com/SeldonIO/MLServer/pull/1467)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.5...1.4.0

[Changes][1.4.0]


<a id="1.3.5"></a>
## [1.3.5](https://github.com/SeldonIO/MLServer/releases/tag/1.3.5) - 2023-07-10

<!-- Release notes generated using configuration in .github/release.yml at 1.3.5 -->

### What's Changed

* Rename HF codec to `hf` by [@adriangonz](https://github.com/adriangonz)  in [#1268](https://github.com/SeldonIO/MLServer/pull/1268)
* Publish is_drift metric to Prom by [@joshsgoldstein](https://github.com/joshsgoldstein)  in [#1263](https://github.com/SeldonIO/MLServer/pull/1263)

### New Contributors
* [@joshsgoldstein](https://github.com/joshsgoldstein) made their first contribution in [#1263](https://github.com/SeldonIO/MLServer/pull/1263)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.4...1.3.5

[Changes][1.3.5]


<a id="1.3.4"></a>
## [1.3.4](https://github.com/SeldonIO/MLServer/releases/tag/1.3.4) - 2023-06-21

<!-- Release notes generated using configuration in .github/release.yml at 1.3.4 -->

### What's Changed

* Silent logging by [@dtpryce](https://github.com/dtpryce) in [#1230](https://github.com/SeldonIO/MLServer/pull/1230)
* Fix `mlserver infer` with `BYTES` by [@RafalSkolasinski](https://github.com/RafalSkolasinski) in [#1213](https://github.com/SeldonIO/MLServer/pull/1213)

### New Contributors
* [@dtpryce](https://github.com/dtpryce) made their first contribution in [#1230](https://github.com/SeldonIO/MLServer/pull/1230)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.3...1.3.4

[Changes][1.3.4]


<a id="1.3.3"></a>
## [1.3.3](https://github.com/SeldonIO/MLServer/releases/tag/1.3.3) - 2023-06-05

<!-- Release notes generated using configuration in .github/release.yml at 1.3.3 -->

### What's Changed

* Add default LD_LIBRARY_PATH env var by [@adriangonz](https://github.com/adriangonz) in [#1120](https://github.com/SeldonIO/MLServer/pull/1120)
* Adding cassava tutorial (mlserver + seldon core) by [@edshee](https://github.com/edshee) in [#1156](https://github.com/SeldonIO/MLServer/pull/1156)
* Add docs around converting to / from JSON by [@adriangonz](https://github.com/adriangonz) in [#1165](https://github.com/SeldonIO/MLServer/pull/1165)
* Document SKLearn available outputs by [@adriangonz](https://github.com/adriangonz) in [#1167](https://github.com/SeldonIO/MLServer/pull/1167) 
* Fix minor typo in `alibi-explain` tests by [@ascillitoe](https://github.com/ascillitoe) in [#1170](https://github.com/SeldonIO/MLServer/pull/1170)
* Add support for `.ubj` models and improve XGBoost docs by [@adriangonz](https://github.com/adriangonz) in  [#1168](https://github.com/SeldonIO/MLServer/pull/1168)
* Fix content type annotations for pandas codecs by [@adriangonz](https://github.com/adriangonz) in  [#1162](https://github.com/SeldonIO/MLServer/pull/1162)
* Added option to configure the grpc histogram by [@cristiancl25](https://github.com/cristiancl25) in [#1143](https://github.com/SeldonIO/MLServer/pull/1143)
* Add OS classifiers to project's metadata by [@adriangonz](https://github.com/adriangonz) in [#1171](https://github.com/SeldonIO/MLServer/pull/1171)
* Don't use `qsize` for parallel worker queue by [@adriangonz](https://github.com/adriangonz) in [#1169](https://github.com/SeldonIO/MLServer/pull/1169)
* Fix small typo in Python API docs by [@krishanbhasin-gc](https://github.com/krishanbhasin-gc)  in [#1174](https://github.com/SeldonIO/MLServer/pull/1174)
* Fix star import in `mlserver.codecs.*` by [@adriangonz](https://github.com/adriangonz) in [#1172](https://github.com/SeldonIO/MLServer/pull/1172)

### New Contributors
* [@cristiancl25](https://github.com/cristiancl25) made their first contribution in [#1143](https://github.com/SeldonIO/MLServer/pull/1143)
* [@krishanbhasin-gc](https://github.com/krishanbhasin-gc) made their first contribution in [#1174](https://github.com/SeldonIO/MLServer/pull/1174)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.2...1.3.3

[Changes][1.3.3]


<a id="1.3.2"></a>
## [1.3.2](https://github.com/SeldonIO/MLServer/releases/tag/1.3.2) - 2023-05-10

<!-- Release notes generated using configuration in .github/release.yml at 1.4.0.dev2 -->

### What's Changed
* Use default initialiser if not using a custom env by [@adriangonz](https://github.com/adriangonz) in [#1104](https://github.com/SeldonIO/MLServer/pull/1104)
* Add support for online drift detectors by [@ascillitoe](https://github.com/ascillitoe) in [#1108](https://github.com/SeldonIO/MLServer/pull/1108)
* added intera and inter op parallelism parameters to the hugggingface … by [@saeid93](https://github.com/saeid93) in [#1081](https://github.com/SeldonIO/MLServer/pull/1081)
* Fix settings reference in runtime docs by [@adriangonz](https://github.com/adriangonz) in [#1109](https://github.com/SeldonIO/MLServer/pull/1109)
* Bump Alibi libs requirements by [@adriangonz](https://github.com/adriangonz) in [#1121](https://github.com/SeldonIO/MLServer/pull/1121)
* Add default LD_LIBRARY_PATH env var by [@adriangonz](https://github.com/adriangonz) in [#1120](https://github.com/SeldonIO/MLServer/pull/1120)
* Ignore both .metrics and .envs folders by [@adriangonz](https://github.com/adriangonz) in [#1132](https://github.com/SeldonIO/MLServer/pull/1132)

### New Contributors
* [@ascillitoe](https://github.com/ascillitoe) made their first contribution in [#1108](https://github.com/SeldonIO/MLServer/pull/1108)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.3.1...1.3.2

[Changes][1.3.2]


<a id="1.3.1"></a>
## [1.3.1](https://github.com/SeldonIO/MLServer/releases/tag/1.3.1) - 2023-04-27

### What's Changed

- Move OpenAPI schemas into Python package ([#1095](https://github.com/SeldonIO/MLServer/issues/1095))

[Changes][1.3.1]


<a id="1.3.0"></a>
## [1.3.0](https://github.com/SeldonIO/MLServer/releases/tag/1.3.0) - 2023-04-27

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
* [@rio](https://github.com/rio) made their first contribution in [#864](https://github.com/SeldonIO/MLServer/pull/864)
* [@pepesi](https://github.com/pepesi) made their first contribution in [#692](https://github.com/SeldonIO/MLServer/pull/692)
* [@jgallardorama](https://github.com/jgallardorama) made their first contribution in [#849](https://github.com/SeldonIO/MLServer/pull/849)
* [@alvarorsant](https://github.com/alvarorsant) made their first contribution in [#860](https://github.com/SeldonIO/MLServer/pull/860)
* [@gawsoftpl](https://github.com/gawsoftpl) made their first contribution in [#950](https://github.com/SeldonIO/MLServer/pull/950)
* [@stephen37](https://github.com/stephen37) made their first contribution in [#1033](https://github.com/SeldonIO/MLServer/pull/1033)
* [@sauerburger](https://github.com/sauerburger) made their first contribution in [#1064](https://github.com/SeldonIO/MLServer/pull/1064)

[Changes][1.3.0]


<a id="1.2.4"></a>
## [1.2.4](https://github.com/SeldonIO/MLServer/releases/tag/1.2.4) - 2023-03-10

<!-- Release notes generated using configuration in .github/release.yml at 1.2.4 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.3...1.2.4

[Changes][1.2.4]


<a id="1.2.3"></a>
## [1.2.3](https://github.com/SeldonIO/MLServer/releases/tag/1.2.3) - 2023-01-16

<!-- Release notes generated using configuration in .github/release.yml at 1.2.3 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.2...1.2.3

[Changes][1.2.3]


<a id="1.2.2"></a>
## [1.2.2](https://github.com/SeldonIO/MLServer/releases/tag/1.2.2) - 2023-01-16

<!-- Release notes generated using configuration in .github/release.yml at 1.2.2 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.1...1.2.2

[Changes][1.2.2]


<a id="1.2.1"></a>
## [1.2.1](https://github.com/SeldonIO/MLServer/releases/tag/1.2.1) - 2022-12-19

<!-- Release notes generated using configuration in .github/release.yml at 1.2.1 -->



**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.2.0...1.2.1

[Changes][1.2.1]


<a id="1.2.0"></a>
## [1.2.0](https://github.com/SeldonIO/MLServer/releases/tag/1.2.0) - 2022-11-25

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
* [@johnpaulett](https://github.com/johnpaulett) made their first contribution in [#633](https://github.com/SeldonIO/MLServer/pull/633)
* [@saeid93](https://github.com/saeid93) made their first contribution in [#711](https://github.com/SeldonIO/MLServer/pull/711)
* [@RafalSkolasinski](https://github.com/RafalSkolasinski) made their first contribution in [#720](https://github.com/SeldonIO/MLServer/pull/720)
* [@dumaas](https://github.com/dumaas) made their first contribution in [#742](https://github.com/SeldonIO/MLServer/pull/742)
* [@Salehbigdeli](https://github.com/Salehbigdeli) made their first contribution in [#776](https://github.com/SeldonIO/MLServer/pull/776)
* [@regen100](https://github.com/regen100) made their first contribution in [#839](https://github.com/SeldonIO/MLServer/pull/839)

**Full Changelog**: https://github.com/SeldonIO/MLServer/compare/1.1.0...1.2.0

[Changes][1.2.0]


<a id="1.1.0"></a>
## [v1.1.0](https://github.com/SeldonIO/MLServer/releases/tag/1.1.0) - 2022-08-01



[Changes][1.1.0]


[1.7.1]: https://github.com/SeldonIO/MLServer/compare/1.7.0...1.7.1
[1.7.0]: https://github.com/SeldonIO/MLServer/compare/1.6.1...1.7.0
[1.6.1]: https://github.com/SeldonIO/MLServer/compare/1.6.0...1.6.1
[1.6.0]: https://github.com/SeldonIO/MLServer/compare/1.5.0...1.6.0
[1.5.0]: https://github.com/SeldonIO/MLServer/compare/1.4.0...1.5.0
[1.4.0]: https://github.com/SeldonIO/MLServer/compare/1.3.5...1.4.0
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
[1.2.0]: https://github.com/SeldonIO/MLServer/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/SeldonIO/MLServer/tree/1.1.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.9.0 -->
