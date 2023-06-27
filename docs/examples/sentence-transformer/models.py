from mlserver import MLModel
from mlserver.types import InferenceRequest, InferenceResponse
from sentence_transformers import SentenceTransformer
from mlserver.codecs import decode_args
from typing import List
import numpy as np 

class SentenceTransformerModel(MLModel):

  async def load(self) -> bool:
    # TODO: Replace for custom logic to load a model artifact
    self._model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return True

  @decode_args
#   async def predict(self, questions: List[str], context: List[str]) -> np.ndarray:
  async def predict(self, questions: List[str]) -> np.ndarray:
    # TODO: Replace for custom logic to run inference
    print(questions)
    return self._model.encode(questions)