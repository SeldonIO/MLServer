# Benchmarking

This folder contains a set of tools to benchmark the gRPC and REST APIs of
`mlserver`.
These load tests are run locally against a local server.

## Current results

|      | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ---- | ------------ | ------------ | ------------ | ------------ |
| gRPC | 2259         | 128.46       | 703.84       | 3.09         |
| REST | 1300         | 226.93       | 304.98       | 2.06         |

## Setup

The benchmark scenarios in this folder leverage [`k6`](https://k6.io/).
To install `k6`, please check their [installation docs
page](https://k6.io/docs/getting-started/installation/):

https://k6.io/docs/getting-started/installation/

## Data

You can find pre-generated requests under the [`/data`](./data) folder.

### Generate

You can re-generate the test requests by using the
[`generator.py`](./generator.py) script:

```shell
python generator.py
```

## Usage

For any load test, the first step will be to spin up the test server, which we
can do with:

```shell
make start-testserver
```

### Inference benchmark

You can kickstart the HTTP and gRPC inference benchmark by running either:

```shell
make benchmark-rest
make benchmark-grpc
```

These will first load a **Scikit-Learn model trained on the Iris dataset**, and
perform an inference benchmark leveraging both the HTTP and gRPC interfaces
(lasting 60s each).
The model has been set up so as to leverage adaptive batching (i.e. grouping
several requests together on the fly).

At the end of the benchmark, the benchmark scenarios will unload the used model
from the MLServer instance.
