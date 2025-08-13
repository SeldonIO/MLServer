# Metrics

The metrics module provides utilities for collecting and exposing metrics
from MLServer instances. This includes performance metrics, health checks,
and operational statistics.

```{autodoc2-object} mlserver.metrics
:renderer: myst
```

## Metrics Collection

MLServer automatically collects various metrics including:

- **Request Counts**: Number of requests processed
- **Response Times**: Latency measurements
- **Error Rates**: Failed request statistics
- **Model Performance**: Inference-specific metrics
- **Resource Usage**: CPU, memory, and GPU utilization

## Prometheus Integration

Metrics are exposed in Prometheus format and can be scraped by monitoring
systems for alerting and visualization. 