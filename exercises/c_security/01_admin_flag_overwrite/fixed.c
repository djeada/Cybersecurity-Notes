#include <stdio.h>
#include <string.h>

struct Account {
    char username[8];
    int is_admin;
};

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s USERNAME\n", argv[0]);
        return 2;
    }

    struct Account account = {{0}, 0};
    size_t length = strlen(argv[1]);
    if (length >= sizeof account.username) {
        fputs("rejected: username too long\n", stderr);
        return 1;
    }
    memcpy(account.username, argv[1], length + 1);
    printf("admin=%d\n", account.is_admin != 0);
    return 0;
}
