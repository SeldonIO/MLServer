from .sys_tracing import SystemTracingProvider

sysTracingProviderName = "mlserver"
sys_tracer: SystemTracingProvider = SystemTracingProvider(sysTracingProviderName)


def configure_tracepoints(sys_tracer: SystemTracingProvider, enable_tracepoints: bool):
    if sys_tracer.tracepoints_count == 0:
        sys_tracer.create_native_sdt_tracepoints(enable_tracepoints)
    return sys_tracer
