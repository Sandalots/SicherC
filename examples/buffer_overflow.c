/* Description: A Simple C Program to raise a buffer overflow 
*  Author: Sandalots
*  Date: 12/03/2025 */

// use the standard io library
#include <stdio.h>

// A Buffer Overflow Test
int main() {
    // declare both a small buffer and a much larger buffer
    char init_buffer[15]; 
    char much_larger_buffer[7788] = "This is a much larger buffer than the initial one! I wonder what could possibly go wrong? A Buffer Overflow, perhaps???";

    // Manually copy the contents of the larger buffer to the smaller buffer
    for (int i = 0; i < 7788; i++) {
        init_buffer[i] = much_larger_buffer[i];
    }

    // output the contents of the smaller buffer
    printf("Buffer contents: %s\n", init_buffer);

    // exit the program
    return 0;
}