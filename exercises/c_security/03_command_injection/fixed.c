#include <stdio.h>
#include <sys/stat.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct stat info;
    if (stat(argv[1], &info) == 0) {
        puts("EXISTS");
    } else {
        puts("MISSING");
    }
    return 0;
}
