# RankLogit
This repository contains code to compute the likelihood function of a discrete logit choice model, proposed by statiscian Paul D. Allison and physician/sociologist Nicholas A. Christakis. It resembles a Multinomial Logit Model, but accomodates for tied choices by permuting the tied items, which (computationally) scales in $O(t!)$ fashion for each observation, where $t$ is the maximum number of tied items at any level. 

Currently, in order to get _ranklogit_ working, one needs Cython, to compile some thinly wrapped C code - which performs the intensive part of the computation - into an importable Python extension. The _misc_ directory contains some other bits and bobs which were used alongside this model in a statistical commercial research project. The Python code is written in OOP, very loosely modelled around scipy and sklearn interfaces. 

There is also a rough example script: _egdriver.py_, in the root directory, which provides some example use of the classes in _ranklogit_ and _misc_. We currently use this script, along with some test files (which are unfortunately gitignored, as they contain sensitive data), to run correctness tests every time this repository recieves updates. 

## Estimation
In the future, this repository _may_ also contain utilities to estimate the model, as the predominating method is with Maximum Likelihood Procedures. Feel free to reach out with any suggestions on the best way to approach this, as we do evaluate the likelihood function fairly efficiently, so it should either be a matter of implementing standard likelihood estimation procedures here, or integrating with an existing Python estimation framework. 

The PHREG procedure in SAS can estimate this model. 

## Other notes
This method of modelling preferences can work well when analyzing data in which the number of discrete choice outcomes does not exceed 10. This form of the model was proposed and explored under sociological contexts, and had original applications in research related to physician decision-making, and end-of-life care. 

Other sociological research, in which instances expresse some individual preference (or indifference) within a discrete set, or data resulting from ranking transformations applied on numeric/ordinal data amongst discrete categories, may lend themselves well to the application of this model. See the references below. 

## Reference
Allison, P.D. and Christakis, N.A. (1994). Logit Models for Sets of Ranked Items. Sociological Methodology, 24, p.199-228. doi: https://doi.org/10.2307/270983.

Link to the paper: https://statisticalhorizons.com/wp-content/uploads/2022/01/AllisonChristakis.pdf

See other: https://docs.displayr.com/wiki/Rank-Ordered_Logit_Model_With_Ties