#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv) {
    unsigned seed = (unsigned)time(NULL);
    if (argc == 2) seed = (unsigned)strtoul(argv[1], NULL, 10);
    /* INTENTIONALLY VULNERABLE: predictably seeded non-crypto PRNG. */
    srand(seed);
    printf("token=%u\n", (unsigned)rand());
    return 0;
}
