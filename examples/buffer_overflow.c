#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    char large_input[50] = "This input is too long!";

    strcpy(buffer, large_input); // No bounds checking, potential buffer overflow

    printf("Buffer contents: %s\n", buffer); 

    return 0;
}