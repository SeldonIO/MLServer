# Benchmarking

This folder contains a set of tools to benchmark the gRPC and REST APIs of
`mlserver`.
These load tests are run locally against a local server.

## Current results

|      | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ---- | ------------ | ------------ | ------------ | ------------ |
| gRPC | 3031.56      | 32.93        | 78.90        | 0.92         |
| REST | 1849.48      | 54.0         | 168.4        | 16.4         |

## Setup

The benchmark scenarios in this folder leverage [`k6`](https://k6.io/).
To install `k6`, please check their [installation docs
page](https://k6.io/docs/getting-started/installation/):

https://k6.io/docs/getting-started/installation/

## Data

You can find pre-generated requests under the [`/data`](./data) folder.
These are formed by payloads with a single input tensor, which varies in length from `1024` to `65536`.

> **NOTE**: To work around some limitations of the previous benchmarking suite,
> we will only be using the smallest payload (i.e. with `1024` tensors) as the
> payload for both gRPC and HTTP.

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

You can kickstart the HTTP and gRPC inference benchmark by running:

```shell
make benchmark
```

This will first load a model trained on the Iris dataset, and perform an
inference benchmark leveraging both the HTTP and gRPC interfaces (lasting 60s
each).
At the end of the benchmark, it will unload the used model from the MLServer
instance.
