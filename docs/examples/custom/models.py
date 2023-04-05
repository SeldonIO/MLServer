import json
import numpyro
import numpy as np

from jax import random
from mlserver import MLModel
from mlserver.codecs import decode_args
from mlserver.utils import get_model_uri
from numpyro.infer import Predictive
from numpyro import distributions as dist
from typing import Optional


class NumpyroModel(MLModel):
    async def load(self) -> bool:
        model_uri = await get_model_uri(self._settings)
        with open(model_uri) as model_file:
            raw_samples = json.load(model_file)

        self._samples = {}
        for k, v in raw_samples.items():
            self._samples[k] = np.array(v)

        self._predictive = Predictive(self._model, self._samples)

        return True

    @decode_args
    async def predict(
        self,
        marriage: Optional[np.ndarray] = None,
        age: Optional[np.ndarray] = None,
        divorce: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        predictions = self._predictive(
            rng_key=random.PRNGKey(0), marriage=marriage, age=age, divorce=divorce
        )

        obs = predictions["obs"]
        obs_mean = obs.mean()

        return np.asarray(obs_mean)

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
