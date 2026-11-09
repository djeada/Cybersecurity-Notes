#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    unsigned char packet[4] = {0, 'c', 'a', 't'};
    packet[0] = (unsigned char)strtoul(argv[1], NULL, 10);
    char output[256];
    /* INTENTIONALLY VULNERABLE: packet has only three data bytes. */
    memcpy(output, packet + 1, packet[0]);
    printf("claimed=%u copied\n", (unsigned)packet[0]);
    return 0;
}
