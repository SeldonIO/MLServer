# Benchmarking

This folder contains a set of tools to benchmark the gRPC and REST APIs of
`mlserver`.
These load tests are run locally against a local server.

## Current results

|      | Requests/sec | Average (ms) | Slowest (ms) | Fastest (ms) |
| ---- | ------------ | ------------ | ------------ | ------------ |
| gRPC | 1183.49      | 40.48        | 189.93       | 0.78         |

## Setup

The gRPC benchmark uses [`ghz`](https://ghz.sh/).
To install the pre-requisites, you can run:

```shell
make install-dev
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
