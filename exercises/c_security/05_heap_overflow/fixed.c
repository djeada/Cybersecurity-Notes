#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    size_t length = strlen(argv[1]);
    if (length >= 16) {
        fputs("rejected: message too long\n", stderr);
        return 1;
    }
    char *message = malloc(16);
    if (!message) { perror("malloc"); return 1; }
    memcpy(message, argv[1], length + 1);
    puts(message);
    free(message);
    return 0;
}
