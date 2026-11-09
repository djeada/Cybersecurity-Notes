#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const char *password = "secret42"; /* toy credential only */
    /* INTENTIONALLY VULNERABLE: compares attacker-supplied length. */
    if (strncmp(argv[1], password, strlen(argv[1])) == 0) {
        puts("ACCESS GRANTED");
    } else {
        puts("DENIED");
    }
    return 0;
}
