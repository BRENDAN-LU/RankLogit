//-----------------------------------------------------------------------------
// This is a slightly modifed, and C-transcribed version of an algorithm
// initially written by James P. Kelly.
//
// It generates permutations for a set of items, and performs a computation. 
// This is the computationally intensive part in the computation of the 
// general likelihood function for any pattern of tied items, proposed by 
// Allison and Christakis (1994).
//
// Currently, the functions in this file are designed to be called from a 
// higher level interface, which do some less intensive processing of the 
// input data before using rankpermute to make computations. 
//-----------------------------------------------------------------------------

#include <stdlib.h>

// Forward declaration of helper functions; see definition below
double prod_shrinking_sum(double* arr, unsigned int len, double D); 
void swap(double* x1, double* x2);

// 'Sociological Methodology', vol.24 1994 p208
// For a fixed k, compute the middle sum 'sigma' term in eqn (8) across all Q_k
//      We note that the second term in the denominator is fixed when k is fixed
//      This term is denoted 'D'
// At this step of the computation, we will have already pre-exponentiated 
// the \mu terms from the calling state, which do not change 
// during this computation.
double sigma_permute(double *arr, unsigned int len, double D) {

    // This uses and iterative version of Heap's algorithm to generate 
    // permutations of arr
    // https://en.wikipedia.org/wiki/Heap%27s_algorithm

    // See wiki link - c is an encoding of the stack state
    unsigned int *c = (unsigned int*)malloc(len * sizeof(unsigned int)); 

    if (c == NULL) {
        return -1;      // error code
    }
    
    for (unsigned int i=0; i<len; ++i) {
        arr[i] = 0;     // initialize stack state encoding to 0's
    }

    double numerator = 1.0; 
    double inv_denominator = prod_shrinking_sum(arr, len, D); 

    // the numerator i constant across all p \in Q_k
    for (unsigned int i=0; i<len; ++i) {
        numerator *= arr[i]; 
    }

    unsigned int i = 1; 
    while (i < len) {

        if (c[i] < i) {

            if (i % 2 == 0) {
                swap(&arr[0], &arr[i]); 
            }

            else {
                swap(&arr[c[i]], &arr[i]); 
            }

        // this is a new permutation - we perform our computation on it
        inv_denominator += prod_shrinking_sum(arr, len, D); 

        c[i] += 1; 
        i = 1;

        }

        else {

            c[i] = 0; 
            i += 1; 

        }

    }

    return numerator * inv_denominator; 

}

void swap(double* x1, double* x2) {

    double temp;
    temp = *x1; 
    *x1 = *x2; 
    *x2 = temp; 

}

// For a fixed p \in Q_k, compute the denominator of the innermost 
// product term. 
// The computation proceeds 'backwards', starting from r=d_k, and iterating
// down to r=1. 
// At the i-th iteration, this saves the sum of the trailing i-th terms 
// when computing the sum in the denominator term - we just need to add new term
double prod_shrinking_sum(double* arr, unsigned int len, double D) {

    double curr_sum = arr[len - 1] + D; 
    double curr_prod = curr_sum; 

    for (unsigned int i=len-2; i >= 0; --i) {

        curr_sum += arr[i]; 
        curr_prod *= curr_sum;

    }

    return 1.0/curr_prod; 

}
