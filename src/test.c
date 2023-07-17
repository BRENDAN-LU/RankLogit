#include <stdlib.h>
#include <stdio.h>
#include "rankpermute.h" 

int main(int argc, char*argv[]) {
    
    printf("Starting \n"); 

    double some_arr[5] = {1,2,3,4,5}; 

    double out; 
    out = sigma_permute(&some_arr[0], 5, 2.3);

    printf("Function gives you: %f\n", out);

    return EXIT_SUCCESS; 
}