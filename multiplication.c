#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <gmp.h>

#define MAX_ITER 100000
#define BITS 10000

int main() {
    double times[MAX_ITER];
    gmp_randstate_t state;
    mpz_t a, b, c;

    gmp_randinit_default(state);
    gmp_randseed_ui(state, time(NULL));
    mpz_inits(a, b, c, NULL);

    

    for (int i = 0; i < MAX_ITER; i++) {
        mpz_urandomb(a, state, BITS);
        mpz_urandomb(b, state, BITS);

        clock_t start = clock();
        
        mpz_mul(c, a, b);

        clock_t end = clock();
        times[i] = (double)(end - start) * 1000.0 / CLOCKS_PER_SEC; // en ms
    }

    
    for (int i = 0; i < MAX_ITER - 1; i++) {
        for (int j = i + 1; j < MAX_ITER; j++) {
            if (times[i] > times[j]) {
                double t = times[i];
                times[i] = times[j];
                times[j] = t;
            }
        }
    }

    
    printf("Min: %f ms\n", times[0]);
    printf("Max: %f ms\n", times[MAX_ITER - 1]);
    printf("Q1 : %f ms\n", times[MAX_ITER / 4]);
    printf("Q2 : %f ms\n", times[MAX_ITER / 2]);
    printf("Q3 : %f ms\n", times[3 * MAX_ITER / 4]);

    mpz_clears(a, b, c, NULL);
    gmp_randclear(state);
    return 0;
}