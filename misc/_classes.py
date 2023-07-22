import numpy.typing as npt
import numpy as np
from typing import Iterable


class LCAMixtureModel:
    """
    Now for a linearly weighted Bayesian mixture model, you can evaluate
    posterior probabilities.
    """

    def __init__(self, models: Iterable, weights: npt.ArrayLike):
        assert len(models) == len(weights), "Different number of models and weights"
        self.nclasses = len(models)
        self.models = models
        self.weights = np.array(weights)

    def predict_proba(self, observation):
        wghted_llhds: list[float] = list(range(self.nclasses))
        llhds = np.array(
            [self.models[i].pmf(observation) for i in range(self.nclasses)]
        )
        wghted_llhds = self.weights * llhds # elementwise product
        norm_factor = np.sum(wghted_llhds)
        return wghted_llhds / norm_factor # elementwise division by scalar

    def predict(self, observation):
        return np.argmax(self.predict_proba(observation)) + 1


class LatentClassSpecificWrapperModel:
    """
    Here, you can wrap up the underlying statistical models used in each of the
    latent classes into one.

    Observations should be a tuple of observation inputs, which are valid inputs
    for the evaluate_llhood functions of the individual models. The number of
    items in both arguments must be the same.
    """

    def __init__(self, models: Iterable):
        self.models = models

    def pmf(self, observations: npt.ArrayLike):
        # observations should be a tuple of valid observations
        llhood: float = 1.0
        for i in range(len(self.models)):
            llhood *= self.models[i].pmf(observations[i])
        return llhood


class GeneralMultinoulliModel:  # multinomial but n=1, hence 'noulli'
    """
    A glorified dictionary in our pipeline.

    The observation integer should correspond to the index of the probabilities
    you provide.
    """

    def __init__(self, probabilities: npt.ArrayLike):  # model parameters
        # e.g. k=2 binomial, k=3 trinomial...
        self.probabilities = probabilities

    def pmf(self, observation: int):
        return self.probabilities[(int)(observation)]
