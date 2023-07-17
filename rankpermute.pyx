"""

Cython wrapper for _rankpermute

"""

import numpy as np

cdef extern from "_rankpermute.c": 
    double sigma_permute(double*, unsigned int, double)

# Python wrapper for backend use in Python module to compute likelihood for 
# generalized tied rank logit model
def _sigma_permute(arr, D): 

    # Cast input into appropriate np array
    cdef double[:] arr_copy = arr.copy().astype(float, order='C')

    # Get the length for our C-level function
    cdef unsigned int arr_size = len(arr_copy)

    # Call function and return computation value 
    return sigma_permute(&arr_copy[0], arr_size, D)