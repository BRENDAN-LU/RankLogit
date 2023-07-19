//-----------------------------------------------------------------------------
// July 2023.
//
// This is a slightly modifed, and C-transcribed version of an algorithm
// initially written by James P. Kelly.
//
// It generates permutations for a set of items, and performs a computation. 
// This is the  intensive part in the computation of the general likelihood
// function for any pattern of tied items, proposed by Allison and Christakis 
// (1994). 
//
// Currently, the functions in this file are designed to be called from a 
// higher level interface, which do some less intensive processing of the 
// input data before using utils to make computations. 
//-----------------------------------------------------------------------------

#include <stdlib.h>
#include "utils.h"

// Some forward declarations; see below for implementations
static inline double pi_shrink_sum(double* arr, unsigned int arrlen, double D); 
static inline void swap(double* x1, double* x2);

// 'Sociological Methodology', vol.24 1994 p208
// For a fixed k, compute the middle sum 'sigma' term in eqn (8) across all Q_k
//      We note that the second term in the denominator is fixed when k is fixed
//      This term is denoted 'D'
// At this step of the computation, we will have already pre-exponentiated 
// the \mu terms from the calling state, which do not change 
// during this computation.
double sigmapermute(double *arr, unsigned int arrlen, double D) {

    // keep compiler happy and not complain about signed/unsigned comparator
    unsigned int i; 

    // This uses and iterative version of Heap's algorithm to generate 
    // permutations of arr
    // https://en.wikipedia.org/wiki/Heap%27s_algorithm

    // See wiki link - c is an encoding of the stack state
    unsigned int *c = (unsigned int*)malloc(arrlen*sizeof(unsigned int)); 

    if (c == NULL) {
        return -1;      // error code
    }
    
    for (i = 0; i < arrlen; ++i) {
        c[i] = 0;     // initialize stack state encoding to 0's
    }

    double numerator = 1.0; 
    double inv_denominator = pi_shrink_sum(arr, arrlen, D); 

    // the numerator i constant across all p \in Q_k
    for (i = 0; i < arrlen; ++i) {
        numerator *= arr[i]; 
    }

    i = 1; 
    while (i < arrlen) {

        if (c[i] < i) {

            if (i % 2 == 0) {
                swap(&arr[0], &arr[i]); 
            }

            else {
                swap(&arr[c[i]], &arr[i]); 
            }

            // this is a new permutation - we perform our computation on it
            inv_denominator += pi_shrink_sum(arr, arrlen, D); 

            c[i] += 1; 
            i = 1;

        }

        else {

            c[i] = 0; 
            i += 1; 

        }

    }

    free(c);
    return numerator * inv_denominator; 
    
}

// For a fixed p \in Q_k, compute the denominator of the innermost 
// product term. 
// The computation proceeds 'backwards', starting from r=d_k, and iterating
// down to r=1. 
// At the i-th iteration, this saves the sum of the trailing i-th terms 
// when computing the sum in the denominator term - we just need to add new term
static inline double pi_shrink_sum(double *arr, unsigned int arrlen, double D) {

    int i; // this needs to be signed otherwise loop below will be infinite
    double curr_sum = arr[arrlen - 1] + D; 
    double curr_prod = curr_sum; 

    for (i = arrlen - 2; i >= 0; --i) {

        curr_sum += arr[i]; 
        curr_prod *= curr_sum;

    }

    return 1.0/curr_prod; 

}

// swap
static inline void swap(double *x1, double *x2) {

    double temp = *x1;
    *x1 = *x2; 
    *x2 = temp; 

}
