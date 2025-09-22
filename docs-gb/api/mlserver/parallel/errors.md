# Module `mlserver.parallel.errors`


## Class `EnvironmentNotFound`


**Description:**
Common base class for all non-exit exceptions.

## Class `WorkerError`


**Description:**
Class used to wrap exceptions raised from the workers.
All stacktrace details will be hidden, and the original class won't be
returned. This is to avoid issues with custom exceptions, like:

    https://github.com/SeldonIO/MLServer/issues/881

## Class `WorkerStop`


**Description:**
Common base class for all non-exit exceptions.
