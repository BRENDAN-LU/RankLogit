from math import exp  # avoid numpy overhead on our small sizes
from typing import Iterable, TypedDict, Tuple

from ._utils import _sigmapermute

CACHE_TIED_THRESHOLD = 8  # cache result if number of ties greater than this


class _TiedTermsCache(TypedDict):
    terms: Tuple[Tuple[int], Tuple[int]]
    sigmapermute: float


class TiedRankingLogitModel:
    """
        Link to paper:
    https://statisticalhorizons.com/wp-content/uploads/2022/01/AllisonChristakis.pdf

        Here, we list some assumptions about the use of this class.

        1) We assume that there are no 'empty' response fields.

        2) We also assume we are exponent-iating a common linear index function
            - with each index weight applied to a possible multinomial choice.
        Refer to 5.1 of the paper, in their provided example.

        3) The parameters input should be an array, with each element
        corresponding to the linear index weight (signed). This ordering of
        categories is arbitrary, but should be the same as the observed_rankings
        input.
            - it will be good to provide, in comments, a mapping of the index
            value in the list to some category names.
            - Refer to page 210 for this mu_ij form

        4) Existimg implementation for estimation: Q estimates it by pivoting on
        one of the outcomes. In our use, parameters[0] == 0 all the time.
        This is not necessary for our computation of the likelihood, though.

        See:
    https://en.wikipedia.org/wiki/Multinomial_logistic_regression#As_a_set_of_independent_binary_regressions

    """

    def __init__(self, parameters: Iterable):
        self.parameters = parameters
        self.j = len(parameters)  # keep record of number of categories
        self.exp_params = [exp(x) for x in parameters]
        self.cache: _TiedTermsCache = dict()
        self.cache_hits = 0

    def pmf(self, observed_ranking: Iterable):
        """
        Valid observation inputs are numeric upwards, to a maximum of j, each in
        the list index corresponding to an outcome specified in the parameters
        input.
        """
        # Integer input currently based on Q CID output format
        # Highest integer corresponds to 'best (first)' ranked variable.
        # Then each subsequent lower integer (does not have to decrease
        # sequentially) is a lower level of preference.

        llhood: float = 1.0  # product of llhoods, so we start with 1
        cache_result = False

        # This ensures we do not get stuck in an infinite loop below,
        # as ensures there are two distinct ranks.
        if len(set(observed_ranking)) == 1:
            return llhood

        enumerated = list(enumerate(observed_ranking))

        # start with highest number in input tuple, and iterate down.
        i = max(observed_ranking)

        while True:  # outer product
            tiedIdxs = [index for index, number in enumerated if number == i]
            if len(tiedIdxs) == 0:
                i -= 1
                continue  # continue through - keep checking for lower integers

            lwrIdxs = [index for index, number in enumerated if number < i]
            if len(lwrIdxs) == 0:
                break  # on the last ranking, and there is no llhood term

            if len(tiedIdxs) >= CACHE_TIED_THRESHOLD:
                key_ = (tuple(tiedIdxs), tuple(lwrIdxs))
                if key_ in self.cache:
                    llhood *= self.cache[key_]
                    self.cache_hits += 1
                    i -= 1 # make sure we decrease iterator before continuing
                    continue
                else:
                    cache_result = True

            tiedTerms = [self.exp_params[i] for i in tiedIdxs]
            lwrTerms = sum([self.exp_params[i] for i in lwrIdxs])

            curr_sigmapermute = _sigmapermute(tiedTerms, lwrTerms)
            llhood *= curr_sigmapermute

            if cache_result:
                self.cache[key_] = curr_sigmapermute

            i -= 1  # iterate down

        return llhood
