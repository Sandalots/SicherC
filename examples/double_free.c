/* Description: A Simple C Program to create a double free  
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdio.h>
#include <stdlib.h> // for malloc and free mm functions

// A Double Free Test
int main() {
    // create a pointer to an integer
    int* ptr = (int*)malloc(sizeof(int));

    // set the value of the pointer to a int value, in this case 77
    *ptr = 77;

    // Let's now free the pointer
    free(ptr); // Free the memory

    // Double free: Freeing the same memory block twice, should prompt a double free error
    free(ptr); 

    // return 0 to end the program
    return 0;
}