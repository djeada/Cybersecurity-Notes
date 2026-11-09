#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    /* A dummy internal value makes the information disclosure reproducible.
     * The attacker controls the format, not this value or its address. */
    const char *internal_note = "DEMO_PRIVATE_VALUE";
    /* INTENTIONALLY VULNERABLE: attacker controls format string. */
    printf(argv[1], internal_note);
    putchar('\n');
    return 0;
}
