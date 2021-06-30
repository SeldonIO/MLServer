import json
import numpyro
import numpy as np

from typing import Dict
from jax import random
from mlserver import MLModel, types
from mlserver.utils import get_model_uri
from numpyro.infer import Predictive
from numpyro import distributions as dist


class NumpyroModel(MLModel):
    async def load(self) -> bool:
        model_uri = await get_model_uri(self._settings)
        with open(model_uri) as model_file:
            raw_samples = json.load(model_file)

        self._samples = {}
        for k, v in raw_samples.items():
            self._samples[k] = np.array(v)

        self._predictive = Predictive(self._model, self._samples)

        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        inputs = self._extract_inputs(payload)
        predictions = self._predictive(rng_key=random.PRNGKey(0), **inputs)

        obs = predictions["obs"]
        obs_mean = obs.mean()

        return types.InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                types.ResponseOutput(
                    name="obs_mean",
                    shape=obs_mean.shape,
                    datatype="FP32",
                    data=np.asarray(obs_mean).tolist(),
                )
            ],
        )

    def _extract_inputs(self, payload: types.InferenceRequest) -> Dict[str, np.ndarray]:
        inputs = {}
        for inp in payload.inputs:
            inputs[inp.name] = np.array(inp.data)

        return inputs

    def _model(self, marriage=None, age=None, divorce=None):
        a = numpyro.sample("a", dist.Normal(0.0, 0.2))
        M, A = 0.0, 0.0
        if marriage is not None:
            bM = numpyro.sample("bM", dist.Normal(0.0, 0.5))
            M = bM * marriage
        if age is not None:
            bA = numpyro.sample("bA", dist.Normal(0.0, 0.5))
            A = bA * age
        sigma = numpyro.sample("sigma", dist.Exponential(1.0))
        mu = a + M + A
        numpyro.sample("obs", dist.Normal(mu, sigma), obs=divorce)
