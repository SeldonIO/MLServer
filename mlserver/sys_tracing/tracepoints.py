"""
A tracepoint is a statically defined marker placed in code to identify
application-level events.

From the perspective of the python application, each tracepoint acts like a
normal function call. When a tracepoint is initialized by the tracing provider,
the prototype of this function call needs to be specified.

Here, we define the list of all possible tracepoints exposed by MLServer, (the
`Tracepoint` enum) together with the arguments that can be passed to them
(returned by `Tracepoint.get_arg_types(self)`) when each type of application
event occurs.

The list of arguments is statically defined for each tracepoint in
`ArgTypeMap._prototypes`.

The subset of tracepoints visible to external tracing users can be restricted in
the MLServer settings, via the `tracepoint_settings.configured_tracepoints`
option.

See `system_tracing.provider` for more details about the actual tracepoint
implementation.
"""
from typing import Optional, Tuple, List
from enum import Enum, IntEnum, auto

# The underlying SDT tracepoint implementation currently only works on x86-64
# architectures. For simplicity, it supports a maximum of 6 tracepoint
# arguments, as the x86-64 calling convention passes the first 6 function
# arguments via registers.
MAX_TRACEPOINT_ARGS = 6


class ArgTypes(IntEnum):
    """
    Encoding of Tracepoint argument types, as required by libstapsdt
    """

    # This matches the ArgTypes enum in stapsdt so it should not be changed. It
    # is re-defined here so as to not depend on stapsdt when tracing is
    # disabled. The values for each argument type are stable and not expected to
    # change.
    noarg = 0
    uint8 = 1
    int8 = -1
    uint16 = 2
    int16 = -2
    uint32 = 4
    int32 = -4
    uint64 = 8
    int64 = -8


class RequestQueueId(IntEnum):
    BatchQueue = 1
    WorkerQueue = 2


class ArgTypeMap(IntEnum):
    """
    Members of this enum give meaningful names to argument types used by
    MLServer tracepoints
    """

    model_name_t = ArgTypes.uint64
    model_version_t = ArgTypes.uint64
    old_model_version_t = ArgTypes.uint64
    pipeline_t = ArgTypes.uint64
    tags_t = ArgTypes.uint64
    queue_len_t = ArgTypes.uint32
    worker_pid_t = ArgTypes.int32


class ArgStatus(Enum):
    Ok = auto()
    TooManyArguments = auto()
    NoPrototypeDefined = auto()


class Tracepoint(Enum):
    """
    The available MLServer tracepoints.

    The tracing provider in `system_tracing.provider` has a number of member
    functions (`tp_*`) for firing the tracepoints declared here when the
    corresponding application-level events take place.

    The tracing provider may also be called directly, passing a member of this
    enum as the first argument, together with the corresponding arguments. The
    types of the tracepoint arguments are statically defined for each Tracepoint
    (see `ArgTypeMap._prototypes`)

    Example:
    ```
    sys_trace = SystemTracingProvider()
    sys_trace.generate_native_sdt_tracepoints(tracepoint_settings) ...

    # Fire the model_load_begin tracepoint via explicit member function:
    trace.tp_model_load_begin(model_name, model_version)

    # The equivalent generic call to be used if the tracepoint does not have
    # an associated tp_* function (typically, during testing and development of
    # new tracepoints)
    sys_trace(Tracepoint.model_load_begin, model_name, model_version)
    ```
    """

    model_load_begin = auto()
    model_load_end = auto()
    model_reload_begin = auto()
    model_reload_end = auto()
    model_unload = auto()
    inference_enqueue_req = auto()
    inference_begin = auto()
    inference_end = auto()

    def all():
        return {t for t in Tracepoint}

    def none():
        return set()

    def get_arg_types(self) -> Tuple[Optional[List[int]], ArgStatus]:
        """
        Returns a (arg_types_list, status) tuple for the current tracepoint. The
        arg_types_list, when not None, defines the function prototype of the
        tracepoint.

        The returned arg_types_list is used by the TracingProvider when
        registering the tracepoints with the underlying native tracepoint
        implementation (libstapsdt). Based on this, libstapsdt dynamically
        generates a shared library in ELF format, with one function
        corresponding to each tracepoint and an ELF note section describing
        where the tracepoint arguments can be found (in which registers) at call
        time.

        Tracepoints may have a maximum of MAX_TRACEPOINT_ARGS arguments. If the
        defined prototype has more, or if the prototype can not be found, this
        will be reflected in the returned ArgStatus. Any ArgStatus different
        from ArgStatus.Ok indicates an error state, albeit some states such as
        ArgStatus.TooManyArguments are recoverable (for example, by ignoring the
        additional arguments).

        The list of arguments used by each tracepoint is currently unstable.
        """
        if self in ArgTypeMap._prototypes:
            if len(ArgTypeMap._prototypes[self]) <= MAX_TRACEPOINT_ARGS:
                return ArgTypeMap._prototypes[self], ArgStatus.Ok
            else:
                return (
                    ArgTypeMap._prototypes[self][0:MAX_TRACEPOINT_ARGS],
                    ArgStatus.TooManyArguments,
                )
        else:
            return None, ArgStatus.NoPrototypeDefined


ArgTypeMap.model_args = [ArgTypeMap.model_name_t, ArgTypeMap.model_version_t]
ArgTypeMap.model_args_reload = [
    ArgTypeMap.model_name_t,
    ArgTypeMap.model_version_t,
    ArgTypeMap.old_model_version_t,
]
ArgTypeMap.queue_args = [ArgTypeMap.model_name_t, ArgTypeMap.queue_len_t]
ArgTypeMap.infer_args = [
    ArgTypeMap.model_name_t,
    ArgTypeMap.pipeline_t,
    ArgTypeMap.tags_t,
    ArgTypeMap.worker_pid_t,
]

# TODO(lucian): Stabilise the tracepoint argument definitions after writing a
# number of external applications using them
#
# Together with the tracepoint names, the prototypes form the public interface
# against which external probing code is developed.
ArgTypeMap._prototypes = {
    Tracepoint.model_load_begin: ArgTypeMap.model_args,
    Tracepoint.model_load_end: ArgTypeMap.model_args,
    Tracepoint.model_reload_begin: ArgTypeMap.model_args_reload,
    Tracepoint.model_reload_end: ArgTypeMap.model_args,
    Tracepoint.model_unload: ArgTypeMap.model_args,
    Tracepoint.inference_enqueue_req: ArgTypeMap.queue_args,
    Tracepoint.inference_begin: ArgTypeMap.infer_args,
    Tracepoint.inference_end: ArgTypeMap.infer_args,
}
