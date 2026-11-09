#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    /* INTENTIONALLY VULNERABLE: attacker controls format string. */
    printf(argv[1]);
    putchar('\n');
    return 0;
}
