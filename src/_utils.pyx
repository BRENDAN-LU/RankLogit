"""

Cython wrapper for C utility functions

"""

import numpy as np

cdef extern from "utils.h": 
    double sigma_permute(double*, unsigned int, double)

# Python interface
def _sigma_permute(arr, D): 

    # Cast input into appropriate np array
    # assuming np.float64 is C double
    cdef double[:] arr_copy = arr.copy(order='C').astype(np.float64)

    # Get the length for our C-level function
    cdef Py_ssize_t arr_size = len(arr_copy)

    # Call function and return computation value 
    # do some explicit type casting to be extra safe
    return <float>sigma_permute(&arr_copy[0], <unsigned int>arr_size, <double>D)
