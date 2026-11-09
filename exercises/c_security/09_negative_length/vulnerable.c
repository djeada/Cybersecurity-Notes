#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int length = atoi(argv[1]);
    if (length > 32) return 1;
    char source[32] = "example";
    char output[32] = {0};
    /* INTENTIONALLY VULNERABLE: negative int becomes size_t. */
    memcpy(output, source, (size_t)length);
    puts(output);
    return 0;
}
