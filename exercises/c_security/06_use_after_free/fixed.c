#include <stdio.h>
#include <stdlib.h>

struct Contact { char name[32]; };

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct Contact *contact = malloc(sizeof *contact);
    if (!contact) return 1;
    snprintf(contact->name, sizeof contact->name, "%s", argv[1]);
    puts(contact->name);
    free(contact);
    contact = NULL;
    return 0;
}
