#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char username[8];
    /* INTENTIONALLY VULNERABLE: may omit terminator. */
    strncpy(username, argv[1], sizeof username);
    printf("user=%s\n", username);
    return 0;
}
