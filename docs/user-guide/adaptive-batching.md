# Adaptive Batching

MLServer includes support to batch requests together transparently on-the-fly.
We refer to this as "adaptive batching", although it can also be known as
"predictive batching".

![](../assets/adaptive-batching.svg)

## Benefits

There are usually two main reasons to adopt adaptive batching:

- **Maximise resource usage**.
  Usually, inference operations are “vectorised” (i.e. are designed to operate
  across batches).
  For example, a GPU is designed to operate on multiple data points at the same
  time.
  Therefore, to make sure that it’s used at maximum capacity, we need to run
  inference across batches.

- **Minimise any inference overhead**.
  Usually, all models will have to _“pay”_ a constant overhead when running any
  type of inference.
  This can be something like IO to communicate with the GPU or some kind of
  processing in the incoming data.
  Up to a certain size, this overhead tends to not scale linearly with the
  number of data points.
  Therefore, it’s in our interest to send as large batches as we can without
  deteriorating performance.

However, these benefits will usually scale only up to a certain point, which is
usually determined by either the infrastructure, the machine learning
framework used to train your model, or a combination of both.
Therefore, to maximise the performance improvements brought in by adaptive
batching it will be important to [configure it with the appropriate values for
your model](#usage).
Since these values are usually found through experimentation, **MLServer won't
enable by default adaptive batching on newly loaded models**.

## Usage

MLServer lets you configure adaptive batching independently for each model
through two main parameters:

- **Maximum batch size**, that is how many requests you want to group together.
- **Maximum batch time**, that is how much time we should wait for new
  requests until we reach our maximum batch size.

### `max_batch_size`

The `max_batch_size` field of the `model-settings.json` file (or
alternatively, the `MLSERVER_MODEL_MAX_BATCH_SIZE` global environment
variable) controls the maximum number of requests that should be grouped
together on each batch.
The expected values are:

- `N`, where `N > 1`, will create batches of up to `N` elements.
- `0` or `1`, will disable adaptive batching.

### `max_batch_time`

The `max_batch_time` field of the `model-settings.json` file (or
alternatively, the `MLSERVER_MODEL_MAX_BATCH_TIME` global environment
variable) controls the time that MLServer should wait for new requests to come
in until we reach our maximum batch size.

The expected format is in seconds, but it will take fractional values.
That is, 500ms could be expressed as `0.5`.

The expected values are:

- `T`, where `T > 0`, will wait `T` seconds at most.
- `0`, will disable adaptive batching.
