from ..sys_tracing import SystemTracingProvider

sysTracingProviderWorkerName = "mlserver"
sys_tracer: SystemTracingProvider = SystemTracingProvider(sysTracingProviderWorkerName)
