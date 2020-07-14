# Docker

Example using Docker to containerise a custom MLServer model.

## Overview

This is an example showing how you can provide your own `Dockerfile` with your
own set of dependencies and your own implementation of the `MLModel` interface.

## Usage

To build the Docker image you can run:

```shell
make build
```

To run the Docker image (exposing the right ports), you can run:

```shell
make run
```
