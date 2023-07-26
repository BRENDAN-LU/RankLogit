# RankLogit
This repository contains code to compute the likelihood function of a discrete logit choice model, proposed by statiscian Paul D. Allison and physician/sociologist Nicholas A. Christakis. It resembles a Multinomial Logit Model, but accomodates for tied choices by permuting the tied items, which (computationally) scales in $O(t!)$ fashion for each observation, where $t$ is the maximum number of tied items at any level. 

In order to get _ranklogit_ working from source here, one needs an appropriate C compiler to to build a Python extension module; this can be done manually, or through Cython, and setuptools. Navigate to the _ranklogit_ directory for more instructions. The Python code is written in OOP, very loosely modelled around scipy and sklearn interfaces. 

There is also a rough example script: _egdriver.py_, in the root directory, which provides some example use of the classes in _ranklogit_ and _misc_. This is the script we use, along with some test files (which are unfortunately gitignored, as they contain sensitive data), to run correctness tests every time this repository recieves updates. 

## Estimation
IN PROGRESS. Soon, this repository _will_ also contain utilities to estimate the model. The PHREG procedure in SAS can estimate this form of the model, by specifying TIES=EXACT. 

## Other notes
_ranklogit_ can work well, and reasonably quickly, when modelling data in which the number of discrete choice outcomes does not exceed 10-15. This form of the model was proposed and explored under sociological contexts, and had original applications in research related to physician decision-making, and end-of-life care. 

Other sociological research, in which instances expresse some individual preference (or indifference) within a discrete set, or data resulting from ranking transformations applied on numeric/ordinal data amongst discrete categories, may lend themselves well to the application of this model. Outside of public health and academia, it is also successfully used in commercial market research contexts, often involving respondents and survey data. See the references below. 

## Reference
Allison, P.D. and Christakis, N.A. (1994). Logit Models for Sets of Ranked Items. Sociological Methodology, 24, p.199-228. doi: https://doi.org/10.2307/270983.

Link to the paper: https://statisticalhorizons.com/wp-content/uploads/2022/01/AllisonChristakis.pdf

See other: https://docs.displayr.com/wiki/Rank-Ordered_Logit_Model_With_Ties