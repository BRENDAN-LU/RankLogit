"""

Really rough miscallaneous adhoc code which was used alongside ranklogit.

The ranklogit model was actually part of a broader mixture model in a project.

"""

import numpy.typing as npt
import numpy as np
from typing import Iterable


class LCAMixtureModel:
    """
    Now for a linearly weighted Bayesian mixture model, you can evaluate 
    posterior probabilities.
    """
    def __init__(self, models: Iterable, linear_weights: npt.ArrayLike):
        assert (len(models) == len(linear_weights)), "Different number of models and weights"
        self.num_classes = len(models)
        self.models = models
        self.priors = linear_weights

    def predict_proba(self, observation):
        # Ensure observation format matches the class specific model in the 
        # mixture model framework
        wghted_llhds: list[float] = list(range(self.num_classes))
        for i in range(self.num_classes):
            wghted_llhds[i] = self.priors[i] * self.models[i].evaluate_llhood(observation)
        denom = sum(wghted_llhds)

        output: list[float] = []
        for i in range(len(wghted_llhds)):
            output[i] = wghted_llhds[i]/denom

        return output

    def predict(self, observation):
        # Ensure observation format matches the class specific model in the 
        # mixture model framework
        weighted_llhoods: list[float] = list(range(self.num_classes))
        for i in range(self.num_classes):
            weighted_llhoods[i] = self.priors[i] * self.models[i].evaluate_llhood(observation)
        denom = sum(weighted_llhoods)

        output: list[float] = list(range(self.num_classes))
        for i in range(self.num_classes):
            output[i] = weighted_llhoods[i] / denom

        return np.argmax(output) + 1


class _LatentClassSpecificWrapperModel:
    """
    Here, you can wrap up the underlying statistical models used in each of the 
    latent classes into one.

    Observations should be a tuple of observation inputs, which are valid inputs 
    for the evaluate_llhood functions of the individual models. The number of 
    items in both arguments must be the same.
    """
    def __init__(self, models: Iterable):
        self.models = models

    def evaluate_llhood(self, observations: npt.ArrayLike):  
        # observations should be a tuple of valid observations
        llhood: float = 1.0
        for i in range(len(self.models)):
            llhood *= self.models[i].evaluate_llhood(observations[i])
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

    def evaluate_llhood(self, observation: int):
        return self.probabilities[int(observation)]
    
