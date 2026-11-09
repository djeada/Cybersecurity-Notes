#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *message = malloc(16);
    if (!message) return 1;
    /* INTENTIONALLY VULNERABLE: ignores the 16-byte capacity. */
    strcpy(message, argv[1]);
    puts(message);
    free(message);
    return 0;
}
