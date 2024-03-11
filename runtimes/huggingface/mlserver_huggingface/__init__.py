from .runtime import HuggingFaceRuntime
from .pipelines import StEmbeddingPipeline
from transformers.pipelines import PIPELINE_REGISTRY

# Added Custom pipeline
PIPELINE_REGISTRY.register_pipeline(
    "sentence-embedding",
    pipeline_class=StEmbeddingPipeline,
    type="text",
)
__all__ = ["HuggingFaceRuntime"]
