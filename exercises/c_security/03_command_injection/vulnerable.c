#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char command[256];
    int n = snprintf(command, sizeof command,
                     "test -e %s && echo EXISTS", argv[1]);
    if (n < 0 || (size_t)n >= sizeof command) return 1;
    /* INTENTIONALLY VULNERABLE: invokes a shell with user data. */
    return system(command) == -1 ? 1 : 0;
}
