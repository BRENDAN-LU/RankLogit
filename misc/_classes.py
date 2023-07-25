from itertools import tee
from math import prod  # quicker than numpy and functools reduce
from operator import mul
from typing import Iterable, List


class LCAMixtureModel:
    """
    Evaluate posterior probabilities for a linear mixture model.
    """

    def __init__(self, models: Iterable, weights: Iterable):
        assert len(models) == len(weights), "Different number of models and weights"
        self.nclasses = len(models)
        self.models = models
        self.weights = weights

    def predict_proba(self, observation: Iterable) -> List[float]:
        wghted_llhds: list[float] = list(range(self.nclasses))
        llhds = [self.models[i].pmf(observation) for i in range(self.nclasses)]
        wghted_llhds, wghted_llhds_copy = tee(map(mul, self.weights, llhds))
        norm_factor = sum(wghted_llhds_copy)
        return [x / norm_factor for x in wghted_llhds]

    def predict(self, observation):
        probs = self.predict_proba(observation)
        return max(range(len(probs)), key=probs.__getitem__) + 1


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

    def pmf(self, observations: Iterable):
        # observations should be a tuple of valid observations
        return prod(
            [self.models[i].pmf(observations[i]) for i in range(len(observations))]
        )


class GeneralMultinoulliModel:  # multinomial but n=1, hence 'noulli'
    """
    A glorified dictionary, to work within the latent class wrapper.

    The observation integer should correspond to the index of the probabilities
    you provide.
    """

    def __init__(self, probabilities: Iterable):  # parameters
        # e.g. len(probabilities)=2 binomial, k=3 trinomial, so on...
        self.probabilities = probabilities

    def pmf(self, observation: int):
        return self.probabilities[(int)(observation)]
