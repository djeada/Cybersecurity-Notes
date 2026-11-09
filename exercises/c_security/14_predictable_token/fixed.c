#define _GNU_SOURCE
#include <errno.h>
#include <stdio.h>
#include <sys/random.h>

/* A 128-bit token is for demonstration; production systems must also
 * securely store, expire and validate tokens. */
int main(void) {
    unsigned char token[16];
    size_t done = 0;
    while (done < sizeof token) {
        ssize_t n = getrandom(token + done, sizeof token - done, 0);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) { perror("getrandom"); return 1; }
        done += (size_t)n;
    }
    fputs("token=", stdout);
    for (size_t i = 0; i < sizeof token; ++i) printf("%02x", token[i]);
    putchar('\n');
    return 0;
}
