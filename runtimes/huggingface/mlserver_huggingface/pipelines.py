from typing import Union, List

from transformers import Pipeline
from transformers import AutoModel
from transformers import AutoTokenizer
from sentence_transformers.util import is_sentence_transformer_model
from sentence_transformers import SentenceTransformer


class StEmbeddingPipeline(Pipeline):
    """A custom huggingface pipeline that wraps sentence transformers embedder"""

    def __init__(self, model: AutoModel,tokenizer:AutoTokenizer, **kwargs):
        # This tokenzier is not being used
        # sentence-transformers model contains a tokenizer 
        self.tokenizer = tokenizer
        (
            self._preprocess_params,
            self._forward_params,
            self._postprocess_params,
        ) = self._sanitize_parameters(**kwargs)
        self.model_name = model.config._name_or_path
        assert is_sentence_transformer_model(
            self.model_name
        ), f"{self.model_name} is not a sentence transformers model."
        self.model = SentenceTransformer(self.model_name)
    def _sanitize_parameters(self, **kwargs):
        forward_kwargs = {}
        if "prompt_name" in kwargs:
            forward_kwargs["prompt_name"] = kwargs["prompt_name"]
        if "prompt" in kwargs:
            forward_kwargs["prompt"] = kwargs["prompt"]
        if "show_progress_bar" in kwargs:
            forward_kwargs["show_progress_bar"] = kwargs["show_progress_bar"]
        if "output_value" in kwargs:
            forward_kwargs["output_value"] = kwargs["output_value"]
        if "convert_to_numpy" in kwargs:
            forward_kwargs["convert_to_numpy"] = kwargs["convert_to_numpy"]
        if "convert_to_tensor" in kwargs:
            forward_kwargs["convert_to_tensor"] = kwargs["convert_to_tensor"]
        if "device" in kwargs:
            forward_kwargs["device"] = kwargs["device"]
        if "normalize_embeddings" in kwargs:
            forward_kwargs["normalize_embeddings"] = kwargs["normalize_embeddings"]
        return {}, forward_kwargs, {}

    def preprocess(self, sentences: Union[str, List[str]]) -> List[str]:
        if isinstance(sentences, str):
            sentences = [sentences]
        return sentences

    def _forward(self, sentences: List[str], batch_size=32, **kwargs):
        outputs = self.model.encode(sentences, batch_size=batch_size, **kwargs)
        return outputs

    def forward(self, sentences: List[str], batch_size=32, **forward_params):
        model_outputs = self._forward(
            sentences, batch_size=batch_size, **forward_params
        )
        return model_outputs

    def postprocess(self, model_outputs):
        outputs = {"embeddings": model_outputs}
        return outputs

    def __call__(self, sentences: Union[str, List[str]], batch_size=32, **kwargs):
        (
            preprocess_params,
            forward_params,
            postprocess_params,
        ) = self._sanitize_parameters(**kwargs)
        # Fuse __init__ params and __call__ params without modifying the __init__ ones.
        preprocess_params = {**self._preprocess_params, **preprocess_params}
        forward_params = {**self._forward_params, **forward_params}
        postprocess_params = {**self._postprocess_params, **postprocess_params}
        sentences = self.preprocess(sentences, **preprocess_params)
        model_outputs = self.forward(sentences, batch_size=batch_size, **forward_params)
        outputs = self.postprocess(model_outputs, **postprocess_params)
        return outputs

    def predict(self, X, batch_size=32, **kwargs):
        return self(X, batch_size=batch_size, **kwargs)
