# Benchmarking

This folder contains a set of tools to benchmark the gRPC and REST APIs of
`mlserver`.
These load tests are run locally against a local server.

## Current results

|      | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ---- | ------------ | ------------ | ------------ | ------------ |
| gRPC | 1183.49      | 40.48        | 189.93       | 0.78         |

## Setup

The gRPC benchmark uses [`ghz`](https://ghz.sh/) and the HTTP benchmark uses
[`hey`](https://github.com/rakyll/hey).
To install the pre-requisites, you can run:

```shell
make install-dev
```

## Data

You can find pre-generated requests under the [`/data`](./data) folder.
These are formed by payloads with a single input tensor, which varies in length
from `1024` to `65536`.

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

The test server will start both the REST and gRPC APIs and will pre-load a test
model which sums over all the elements of the input and returns the total as a
result.

### gRPC

To run the gRPC benchmark:

```shell
make benchmark-grpc
```

This will run 10000 requests across 10 connections shared by 50 workers.
