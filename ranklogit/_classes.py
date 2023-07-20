import numpy.typing as npt
import numpy as np

from ._utils import _sigmapermute


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

    def __init__(self, parameters: npt.ArrayLike):
        self.parameters = np.asarray(parameters)
        self.j = len(parameters)  # keep record of number of categories

        self.exp_params = np.exp(self.parameters)

    def pmf(self, observed_ranking: npt.ArrayLike):
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

            else:
                lwrIdxs = [index for index, number in enumerated if number < i]
                if len(lwrIdxs) == 0:
                    break  # on the last ranking, and there is no llhood term

                tiedTerms = self.exp_params[tiedIdxs]
                lwrTerms = np.sum(self.exp_params[lwrIdxs])

                llhood *= _sigmapermute(tiedTerms, lwrTerms)
                i -= 1  # iterate down

        return llhood
