#include <stdlib.h>

int main(void) {
    int *task = malloc(sizeof *task);
    if (!task) return 1;
    *task = 42;
    free(task);
    /* INTENTIONALLY VULNERABLE: duplicate cleanup. */
    free(task);
    return 0;
}
