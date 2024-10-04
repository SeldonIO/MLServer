# Parallel Inference

Out of the box, MLServer includes support to offload inference workloads to a
pool of workers running in separate processes.
This allows MLServer to scale out beyond the limitations of the Python
interpreter.
To learn more about why this can be beneficial, you can check the [concurrency
section](#concurrency-in-python) below.

![](../images/parallel-inference.svg)

By default, MLServer will spin up a pool with only one worker process to run
inference.
All models will be loaded uniformly across the inference pool workers.
To read more about advanced settings, please see the [usage section
below](#usage).

## Concurrency in Python

The [Global Interpreter Lock (GIL)](https://wiki.python.org/moin/GlobalInterpreterLock) 
is a mutex lock that exists in most Python interpreters (e.g. CPython).
Its main purpose is to lock Python’s execution so that it only runs on a single
processor at the same time.
This simplifies certain things to the interpreter.
However, it also adds the limitation that a **single Python process will never
be able to leverage multiple cores**.

When we think about MLServer's support for [Multi-Model Serving (MMS)](../examples/mms/README.md), 
this could lead to scenarios where a
**heavily-used model starves the other models** running within the same
MLServer instance.
Similarly, even if we don’t take MMS into account, the **GIL also makes it harder
to scale inference for a single model**.

To work around this limitation, MLServer offloads the model inference to a pool
of workers, where each worker is a separate Python process (and thus has its
own separate GIL).
This means that we can get full access to the underlying hardware.

### Overhead

Managing the Inter-Process Communication (IPC) between the main MLServer
process and the inference pool workers brings in some overhead.
Under the hood, MLServer uses the `multiprocessing` library to implement the
distributed processing management, which has been shown to offer the smallest
possible overhead when implementing these type of distributed strategies
{cite}`zhiFiberPlatformEfficient2020`.

The extra overhead introduced by other libraries is usually brought in as a
trade off in exchange of other advanced features for complex distributed
processing scenarios.
However, MLServer's use case is simple enough to not require any of these.

Despite the above, even though this overhead is minimised, this **it can still
be particularly noticeable for lightweight inference methods**, where the extra
IPC overhead can take a large percentage of the overall time.
In these cases (which can only be assessed on a model-by-model basis), the user
has the option to [disable the parallel inference feature](#usage).

For regular models where inference can take a bit more time, this overhead is
usually offset by the benefit of having multiple cores to compute inference on.

## Usage

By default, MLServer will always create an inference pool with one single worker.
The number of workers (i.e. the size of the inference pool) can be adjusted
globally through the server-level `parallel_workers` setting.

### `parallel_workers`

The `parallel_workers` field of the `settings.json` file (or alternatively, the
`MLSERVER_PARALLEL_WORKERS` global environment variable) controls the size of
MLServer's inference pool.
The expected values are:

- `N`, where `N > 0`, will create a pool of `N` workers.
- `0`, will disable the parallel inference feature.
  In other words, inference will happen within the main MLServer process.

## References

Jiale Zhi, Rui Wang, Jeff Clune, and Kenneth O. Stanley. Fiber: A Platform for Efficient Development and Distributed Training for Reinforcement Learning and Population-Based Methods. arXiv:2003.11164 [cs, stat], March 2020. [arXiv:2003.11164](https://arxiv.org/abs/2003.11164).