/* Description: A Simple C Program to create a double free  
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdio.h>
#include <stdlib.h>

// A Double Free Test
int main() {
    int* ptr = (int*)malloc(sizeof(int));
    *ptr = 42;

    free(ptr); // Free the memory

    // Double free: Freeing the same memory block twice
    free(ptr); 

    return 0;
}