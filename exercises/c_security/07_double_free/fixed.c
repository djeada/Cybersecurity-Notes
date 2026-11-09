#include <stdlib.h>

int main(void) {
    int *task = malloc(sizeof *task);
    if (!task) return 1;
    *task = 42;
    /* One owning cleanup path; no second free. */
    free(task);
    task = NULL;
    return 0;
}
