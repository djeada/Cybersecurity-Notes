#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char path[256];
    int n = snprintf(path, sizeof path, "notes/%s", argv[1]);
    if (n < 0 || (size_t)n >= sizeof path) return 1;
    /* INTENTIONALLY VULNERABLE: traversal is not blocked. */
    FILE *file = fopen(path, "r");
    if (!file) { perror("fopen"); return 1; }
    char line[128];
    if (fgets(line, sizeof line, file)) fputs(line, stdout);
    fclose(file);
    return 0;
}
