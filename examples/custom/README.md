# Custom model

Example serving a custom model.

## Overview

This is an example of how you can implement a custom model interface to serve
your own model.

## Usage

To start serving your model, you can run:

```shell
mlserver start .
```

## Building

To build a Docker image, you can simply run:

```shell
mlserver bundle .
cd _bundle
docker build .
```

The `mlserver bundle` will wrap your model's contents into a `_bundle` folder
which can be used as-is to build a Docker image.
