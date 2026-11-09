#include <stdio.h>

int main(void) {
    /* INTENTIONALLY VULNERABLE: follows a preexisting symlink. */
    FILE *file = fopen("scratch/report.tmp", "w");
    if (!file) { perror("fopen"); return 1; }
    fputs("REPORT\n", file);
    if (fclose(file) != 0) return 1;
    return 0;
}
