#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Contact { char name[32]; };

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    struct Contact *contact = malloc(sizeof *contact);
    if (!contact) return 1;
    snprintf(contact->name, sizeof contact->name, "%s", argv[1]);
    free(contact);
    /* INTENTIONALLY VULNERABLE: contact's lifetime has ended. */
    puts(contact->name);
    return 0;
}
