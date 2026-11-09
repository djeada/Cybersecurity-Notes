#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    unsigned long count = strtoul(argv[1], NULL, 10);
    if (count == 0 || count > 10000) return 2;
    /* INTENTIONALLY VULNERABLE: truncates a byte count to 16 bits. */
    uint16_t bytes = (uint16_t)(count * 16UL);
    char *records = malloc(bytes);
    if (!records) return 1;
    printf("allocated=%u requested=%lu\n", (unsigned)bytes, count * 16UL);
    fflush(stdout);
    memset(records, 'X', (size_t)count * 16U);
    free(records);
    return 0;
}
