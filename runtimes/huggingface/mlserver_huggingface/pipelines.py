from typing import Union, List

from transformers import Pipeline
from transformers import AutoModel
from sentence_transformers.util import is_sentence_transformer_model
from sentence_transformers import SentenceTransformer


class StEmbeddingPipeline(Pipeline):
    """A custom huggingface pipeline that wraps sentence transformers embedder"""

    def __init__(self, model: AutoModel, **kwargs):
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

    def preprocess(self, sentences: Union[str, List[str]]):
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
        """
        Computes sentence embeddings.

        Parameters
        ----------
        sentences: str
            the sentences to embed.
        prompt_name: dict
            The name of the prompt to use for encoding. Must be a key in the `prompts` dictionary
            which is either set in the constructor or loaded from the model configuration. For example if
            `prompt_name` is ``"query"`` and the `prompts` is ``{"query": "query: ", ...}``, then the sentence "What
            is the capital of France?" will be encoded as "query: What is the capital of France?" because the sentence
            is appended to the prompt. If `prompt` is also set, this argument is ignored.
        prompt: str
            The prompt to use for encoding. For example, if the prompt is ``"query: "``, then the
            sentence "What is the capital of France?" will be encoded as "query: What is the capital of France?"
            because the sentence is appended to the prompt. If `prompt` is set, `prompt_name` is ignored.
        batch_size: int
            the batch size used for the computation.
        show_progress_bar: bool
            Whether to output a progress bar when encode sentences.
        output_value: str
            The type of embeddings to return: "sentence_embedding" to get sentence embeddings,
            "token_embeddings" to get wordpiece token embeddings, and `None`, to get all output values. Defaults
            to "sentence_embedding".
        convert_to_numpy: bool
            Whether the output should be a list of numpy vectors. If False, it is a list of PyTorch tensors.
        convert_to_tensor: bool
            Whether the output should be one large tensor. Overwrites `convert_to_numpy`.
        device: str
            Which `torch.device` to use for the computation.

        normalize_embeddings: bool
            Whether to normalize returned vectors to have length 1. In that case,
            the faster dot-product (util.dot_score) instead of cosine similarity can be used.
        Returns
        -------
            By default, a list of tensors is returned. If convert_to_tensor, a stacked tensor is returned.
            If convert_to_numpy, a numpy matrix is returned.

        """
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
