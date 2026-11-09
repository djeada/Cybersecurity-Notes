#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const char *password = "secret42"; /* demonstration, not real password storage */
    if (strcmp(argv[1], password) == 0) {
        puts("ACCESS GRANTED");
    } else {
        puts("DENIED");
    }
    return 0;
}
