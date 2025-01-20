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