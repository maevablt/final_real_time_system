#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <gmp.h> // GNU Multiple Precision Arithmetic Library

#define MAX_ITER 100000 // Number of iterations 
#define BITS 10000      // Size of the integers to multiply (10,000 bits)

int main() {
    double times[MAX_ITER]; // Array to store execution time of each iteration
    gmp_randstate_t state;  // State for the random number generator
    mpz_t a, b, c;          // variables (a, b for operands, c for result)

    
    gmp_randinit_default(state);  // Initialize the random generator with a default algorithm
    gmp_randseed_ui(state, time(NULL));// Seed the generator with the current time to ensure different numbers each run
    
   
    mpz_inits(a, b, c, NULL); // Initialize the variables

    for (int i = 0; i < MAX_ITER; i++) {
        // Generate two random integers of 10,000 bits each
        mpz_urandomb(a, state, BITS);
        mpz_urandomb(b, state, BITS);

        clock_t start = clock(); // Capture the CPU clock cycles before multiplication
        mpz_mul(c, a, b); // Execute the multiplication with the big variables
        clock_t end = clock(); // Capture the CPU clock cycles after multiplication      
        
        times[i] = (double)(end - start) * 1000.0 / CLOCKS_PER_SEC; // Convert the duration to milliseconds (ms) and store it
    }

    
    // Bubble Sort: Organizing the results
    for (int i = 0; i < MAX_ITER - 1; i++) {
        for (int j = i + 1; j < MAX_ITER; j++) {
            if (times[i] > times[j]) {
                double t = times[i];
                times[i] = times[j];
                times[j] = t;
            }
        }
    }

    printf("Min: %f ms\n", times[0]);                     // Minimum Execution Time
    printf("Max: %f ms\n", times[MAX_ITER - 1]);          // WCET
    printf("Q1 : %f ms\n", times[MAX_ITER / 4]);          // First Quartile (25%)
    printf("Q2 : %f ms\n", times[MAX_ITER / 2]);          // Median (50%)
    printf("Q3 : %f ms\n", times[3 * MAX_ITER / 4]);      // Third Quartile (75%)

    mpz_clears(a, b, c, NULL); // Free the memory allocated for BigInts and random state
    gmp_randclear(state);

    return 0;
}