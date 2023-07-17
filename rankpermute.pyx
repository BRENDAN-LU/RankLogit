"""

Cython wrapper for _rankpermute

"""

import numpy as np

cdef extern from "_rankpermute.c": 
    double sigma_permute(double *arr, unsigned int len, double D)

