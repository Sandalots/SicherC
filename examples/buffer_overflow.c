#include <stdio.h>
#include <string.h>

// A Buffer Overflow Test
int main() {
    char init_buffer[15];
    char much_larger_buffer[7788] = "This is a much larger buffer than the initial one! I wonder what could possibly go wrong? A Buffer Overflow, perhaps???";

    strcpy(init_buffer, much_larger_buffer); // copying a larger bugger from a smaller one

    printf("Buffer contents: %s\n", init_buffer);

    return 0;
}