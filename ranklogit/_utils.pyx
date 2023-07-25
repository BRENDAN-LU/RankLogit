"""

Cython wrapper for C utility function

"""

from libc.stdlib cimport malloc, free

cdef extern from "src/utils.h": 
    double sigmapermute(double*, unsigned int, double)

# Python interface; internal use C-speed helper function 
def _sigmapermute(list_, D): 

    # capture list length
    cdef unsigned int arrlen = <unsigned int>len(list)

    # allocate memory for contiguous array data copy over
    cdef double* arr = <double*>malloc(arrlen * sizeof(double))

    # iterate list and copy over data
    cdef unsigned int i
    for i in range(arrlen):
        arr[i] = list_[i]
    
    # pass pointer and length into C level function
    # store the result, so we can free memory before returning
    float result = <float>sigmapermute(&arr[0], arrlen, <double>D)

    free(arr) # release the memory

    return result