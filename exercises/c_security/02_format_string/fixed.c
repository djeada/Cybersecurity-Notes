#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    /* The format string is fixed; input is always data. */
    printf("%s\n", argv[1]);
    return 0;
}
