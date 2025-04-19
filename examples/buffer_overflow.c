/* Description: A Simple C Program to raise a buffer overflow 
*  Author: Sandalots
*  Date: 12/03/2025 */

// use the standard io library
#include <stdio.h>

// A Buffer Overflow Test
int main() {
    // declare both a small buffer and a much larger buffer
    char init_buffer[15];  // smaller buffer
    char much_larger_buffer[7788];  // larger buffer

    // fill the smaller buffer with the contents of the larger buffer
    memcpy(init_buffer, much_larger_buffer, sizeof(much_larger_buffer));

    // output the contents of the smaller buffer
    printf("Buffer contents: %s\n", init_buffer);

    // exit the program
    return 0;
}