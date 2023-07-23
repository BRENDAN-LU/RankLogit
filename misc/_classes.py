import numpy.typing as npt
import numpy as np
from typing import Iterable


class LCAMixtureModel:
    """
    Evaluate posterior probabilities for a linear mixture model.
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
        wghted_llhds = self.weights * llhds  # elementwise product
        norm_factor = np.sum(wghted_llhds)
        return wghted_llhds / norm_factor  # elementwise division by scalar

    def predict(self, observation):
        return np.argmax(self.predict_proba(observation)) + 1


class LatentClassSpecificWrapperModel:
    """
    Wrap independent statistical models, for different features of an
    observation, into one. This represents the model for one latent class.

    Observations should be an Iterable of observation inputs, which are valid
    inputs for the pmf functions of the individual models. The number of
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
    A glorified dictionary, to work within the latent class wrapper.

    The observation integer should correspond to the index of the probabilities
    you provide.
    """

    def __init__(self, probabilities: npt.ArrayLike):  # parameters
        # e.g. len(probabilities)=2 binomial, k=3 trinomial, so on...
        self.probabilities = probabilities

    def pmf(self, observation: int):
        return self.probabilities[(int)(observation)]
