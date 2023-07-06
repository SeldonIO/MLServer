from .logging import logger
from .settings import TracepointSettings
from .sys_tracing import SystemTracingProvider

sysTracingProviderName = "mlserver"
sys_tracer: SystemTracingProvider = SystemTracingProvider(sysTracingProviderName)


def configure_tracepoints(
    sys_tracer: SystemTracingProvider, tracepoint_settings: TracepointSettings
):
    if sys_tracer.tracepoints_count == 0:
        sys_tracer.create_native_sdt_tracepoints(tracepoint_settings)
    return sys_tracer
