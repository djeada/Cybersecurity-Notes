#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    errno = 0;
    char *end;
    unsigned long input = strtoul(argv[1], &end, 10);
    if (errno || end == argv[1] || *end != '\0' ||
        argv[1][0] < '0' || argv[1][0] > '9' ||
        input > UCHAR_MAX) {
        fputs("rejected: invalid length byte\n", stderr);
        return 1;
    }
    unsigned char packet[4] = {0, 'c', 'a', 't'};
    packet[0] = (unsigned char)input;
    char output[256];
    size_t claimed = packet[0];
    size_t available = sizeof packet - 1;
    if (claimed > available || claimed > sizeof output) {
        fputs("rejected: truncated packet\n", stderr);
        return 1;
    }
    memcpy(output, packet + 1, claimed);
    printf("copied=%zu\n", claimed);
    return 0;
}
