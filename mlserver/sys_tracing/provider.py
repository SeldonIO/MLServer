"""
A system tracing provider is the entity responsible for registering and managing
a set of tracepoints that are then visible to external tracing tools. Such tools
may register probes (e.g. Systemtap probes, BPF code) to snapshot performance
counters, debug performance issues, link application activity to kernel actions
or compute various aggregate metrics.

MLServer fires the tracepoints defined by the tracing provider (one of the tp_*
functions) whenever application-specific events take place, such as starting to
process an inference request, loading/unloading a model, etc:

``` 
sys_trace = SystemTracingProvider()
sys_trace.generate_native_sdt_tracepoints(settings.tracepoint_settings) 
... 
# A new model gets loaded
ext_trace.tp_model_load_begin(...) 
model.ready = await model.load() 
ext_trace.tp_model_load_end(...) 
```

Sometimes, the arguments that we want to pass to a tracepoint are obtained by
some processing, which might be expensive. We do not want to pay this cost even
when no external probe is attached to that tracepoint. In this case, we can
first call the `is_active` member function, which only returns true if the
passed tracepoint has an external probe attached:

``` 
if sys_trace.is_active(Tracepoint.inference_begin):
    # compute arguments 
    pipeline = parse_headers(...)

    # fire tracepoint 
    sys_trace.tp_inference_begin(..., pipeline, ...)
```

Each tp_* function calls into a native shared library that is generated on the
fly and dynamically loaded inside the process when calling
`ext_trace.generate_native_sdt_tracepoints(...)`. In the shared library, a
tracepoint is just a hook function (a series of nop instructions followed by a
ret). The code of this hook can be modified at runtime to jump into code
provided from outside the process (e.g. SystemTap or BPF probes running in
kernel context).

When no probe is attached, a tracepoint adds almost no overhead (the cost of a
function call and a branch instruction). When a probe is attached, the process
will incur a mode switch (~5-10 us) each time the probe fires, plus the overhead
of the probing code.

At the moment, tracing is only available on x86-64 architectures.
"""
from importlib import import_module

from ..logging import logger
from ..settings import TracepointSettings
from ..types import Tracepoint, ArgStatus, MAX_TRACEPOINT_ARGS
from .stapsdt_stub import Probe as NopTracepoint


class SystemTracingProvider:
    def __init__(self, name):
        # Tracing is an optional facility, requiring additional runtime
        # dependencies. Because of this, we initialize this provider with stub
        # tracepoints which do nothing.
        #
        # When tracing is enabled via MLServer settings, the actual tracepoint
        # insertion will happen during the `create_native_sdt_tracepoints()`
        # call.
        stapsdt = import_module(".stapsdt_stub", "mlserver.sys_tracing")
        self._name = name

        self._provider = stapsdt.Provider(self._name)
        self._num_native_tracepoints: int = 0
        self._configured_tracepoints: set[Tracepoint] = Tracepoint.none()
        self._tracepoint_definition: dict[
            Tracepoint, stapsdt.Probe | NopTracepoint
        ] = {}

        for tp in Tracepoint:
            self._tracepoint_definition[tp] = NopTracepoint

    def create_native_sdt_tracepoints(self, tracepoint_settings: TracepointSettings):
        """
        Makes the configured tracepoints visible to external tracing programs

        In the underlying implementation, this:
            - generates native shared library with the tracepoints and a
              .notes ELF section with metadata used for attaching probes
            - loads the shared library in the current process
        """
        if tracepoint_settings.enable_tracepoints:
            try:
                # On import, stapsdt will attempt to dynamically load
                # libstapsdt.so, which is responsible for dynamically creating a
                # native ELF library containing the tracepoint functions to
                # which external probes can be attached to.
                import stapsdt
            except:
                logger.warning(
                    "Could not enable tracing. Ensure python-stapsdt and libstapsdt.so are installed"
                )
                return

            self._provider = stapsdt.Provider(self._name)
            self._configured_tracepoints = set(
                tracepoint_settings.configured_tracepoints or Tracepoint.none()
            )

            # The tracepoints configured in settings get registered with the
            # provider, while disabled ones remain as stubs
            for tp in self._configured_tracepoints:
                arg_types, status = tp.get_arg_types()
                if arg_types != None:
                    self._num_native_tracepoints += 1
                    self._tracepoint_definition[tp] = self._provider.add_probe(
                        tp.name, *arg_types
                    )
                if status == ArgStatus.TooManyArguments:
                    logger.warning(
                        f"The prototype for tracepoint {tp.name} has too many arguments (max: {MAX_TRACEPOINT_ARGS}): \
                        only the first {MAX_TRACEPOINT_ARGS} will be considered"
                    )
                elif status == ArgStatus.NoPrototypeDefined:
                    logger.warning(
                        f"Could not register tracepoint {tp.name}, as it has has no defined prototype."
                    )

            # Generate and load the shared object library containing the native
            # tracepoints; remove tracepoints if loading fails
            load_error = self._provider.load()
            if load_error:
                self._num_native_tracepoints = 0
                for tp in self._configured_tracepoints:
                    self._tracepoint_definition[tp] = NopTracepoint

    @property
    def tracepoints_count(self) -> int:
        return self._num_native_tracepoints

    @property
    def name(self) -> str:
        return self._name

    def is_active_for(self, tracepoint: Tracepoint) -> bool:
        """
        Returns true only when there are active external probes attached to the
        given tracepoint

        Importantly, this can be used before calling a tracepoint, when it is
        expensive to compute some of the arguments passed to it and we want to
        avoid incurring that cost all the time.

        The overall pattern for calling a tracepoint in this case becomes:

        ```
        if(sys_trace.is_active(Tracepoint.inference_begin)) {
            // compute arguments
            pipeline = headers.parse(...)

            // fire probe
            sys_trace.tp_inference_begin(..., pipeline, ..)
        }
        ```

        In the underlying implementation, one of the nop instructions of the
        tracepoint hook is replaced by a trap instruction whenever a probe is
        attached. For non-stub tracepoints, the current function checks for the
        existence of the trap instruction. Stub tracepoints will always return
        false.
        """
        return self._tracepoint_definition[tracepoint].is_enabled()

    # Explicit function definitions for each tracepoint
    #
    # These should be preferred to the generic __call__ below, as they constrain
    # the number of arguments and explicitly define the tracing interface for
    # external consumers
    def tp_model_load_begin(self, model_name, model_version) -> bool:
        return self._tracepoint_definition[Tracepoint.model_load_begin].fire(
            model_name, model_version
        )

    def tp_model_load_end(self, model_name, model_version) -> bool:
        return self._tracepoint_definition[Tracepoint.model_load_end].fire(
            model_name, model_version
        )

    def tp_model_reload_begin(
        self, model_name, model_version, old_model_version
    ) -> bool:
        return self._tracepoint_definition[Tracepoint.model_reload_begin].fire(
            model_name, model_version, old_model_version
        )

    def tp_model_reload_end(self, model_name, model_version) -> bool:
        return self._tracepoint_definition[Tracepoint.model_reload_end].fire(
            model_name, model_version
        )

    def tp_model_unload(self, model_name, model_version) -> bool:
        return self._tracepoint_definition[Tracepoint.model_unload].fire(
            model_name, model_version
        )

    def tp_inference_enqueue_req(self, model_name, queue_len) -> bool:
        return self._tracepoint_definition[Tracepoint.inference_enqueue_req].fire(
            model_name, queue_len
        )

    def tp_inference_begin(self, model_name, pipeline, tags, worker_pid) -> bool:
        return self._tracepoint_definition[Tracepoint.inference_begin].fire(
            model_name, pipeline, tags, worker_pid
        )

    def tp_inference_end(self, model_name, pipeline, tags, worker_pid) -> bool:
        return self._tracepoint_definition[Tracepoint.inference_end].fire(
            model_name, pipeline, tags, worker_pid
        )

    # Generic tracepoint event, without constraining the number of arguments
    # Mostly here for use during the creation of new tracepoints, for which
    # specialised tp_* functions do not exist.
    def __call__(self, tracepoint: Tracepoint, *args) -> bool:
        return self._tracepoint_definition[tracepoint].fire(*args)

    def unload(self) -> bool:
        for tp in Tracepoint:
            self._tracepoint_definition[tp] = NopTracepoint
        return self._provider.unload()
