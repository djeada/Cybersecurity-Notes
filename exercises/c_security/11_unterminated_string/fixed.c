#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char username[8];
    size_t length = strlen(argv[1]);
    if (length >= sizeof username) {
        fputs("rejected: username too long\n", stderr);
        return 1;
    }
    memcpy(username, argv[1], length + 1);
    printf("user=%s\n", username);
    return 0;
}
