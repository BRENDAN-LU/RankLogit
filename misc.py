"""
Some other misc adhoc code which we used alongside ranklogit.

The ranklogit model was actually part of a broader mixture model, 
conducting a "latent class analysis". 
"""

import numpy as np
from typing import Tuple 

class LatentClassSpecificWrapperModel:
    """
    Here, you can wrap up the underlying statistical models used in each of the 
    latent classes into one.

    Observations should be a tuple of observation inputs, which are valid inputs 
    for the evaluate_llhood functions of the individual models. The number of 
    items in both arguments must be the same.
    """
    def __init__(self, models: Tuple):
        self.models = models

    def evaluate_llhood(self, observations: Tuple):  
        # observations should be a tuple of valid observations
        llhood: float = 1.0
        for i in range(len(self.models)):
            llhood *= self.models[i].evaluate_llhood(observations[i])
        return llhood


class LCAMixtureModel:
    """
    Now for a linearly weighted Bayesian mixture model, you can evaluate 
    posterior probabilities.
    """
    def __init__(self, classes: int, models: Tuple, linear_weights: Tuple[float, ...]):
        self.num_classes = classes
        self.models = models
        self.priors = linear_weights

    def evaluate_posterior_probability(self, observation):
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

    def label_observation(self, observation):
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
    
    
class GeneralMultinoulliModel:  # multinomial but n=1, hence 'noulli'
    """
    The observation integer should correspond to the index of the probabilities
    you provide. 
    """
    def __init__(self, k: int, probabilities: Tuple[float, ...]):  # model parameters
        # e.g. k=2 binomial, k=3 trinomial...
        # in the probability parameter vector, you NEED to specify
        # one explicit probability for each outcome
        self.k = k
        self.probabilities = probabilities
        self.valid_init = 0
        
    def check_valid_init(self):
        """
        Call before using this function object to ensure valid initialisation of the
        underlying statistical model (correct observation, parameters, so forth)
        """
        num_probabilities_inputted = len(self.probabilities)
        if num_probabilities_inputted == self.k and sum(self.probabilities) == 1:
            self.valid_init = 1

    def evaluate_llhood(self, observation: int):
        """
        Returns None is the observation is not a valid input
        """
        if observation not in list(range(len(self.probabilities))):
            return None
        llhood = self.probabilities[int(observation)]
        return llhood
    
