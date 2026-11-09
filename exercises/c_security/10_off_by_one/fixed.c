#include <stdio.h>

int main(void) {
    volatile char buffer[16];
    for (size_t i = 0; i < sizeof buffer; ++i) {
        buffer[i] = 'A';
    }
    puts("done");
    return 0;
}
