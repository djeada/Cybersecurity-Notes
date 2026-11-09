#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    errno = 0;
    char *end;
    long length = strtol(argv[1], &end, 10);
    if (errno || end == argv[1] || *end != '\0' ||
        length < 0 || length > 32) {
        fputs("rejected: invalid length\n", stderr);
        return 1;
    }
    char source[32] = "example";
    char output[33] = {0};
    memcpy(output, source, (size_t)length);
    puts(output);
    return 0;
}
