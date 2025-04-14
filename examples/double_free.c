/* Description: A Simple C Program to create a double free  
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdio.h>
#include <stdlib.h> // for malloc and free mm functions

// A Double Free Test
int main() {
    // the temp value to be passed to the pointer
    int value = 77; // the value of the integer

    // set the value of the pointer to a int value, in this case 77
    int* ptr = &value; // create a pointer to the integer value

    // Let's now free the pointer
    free(ptr); // Free the memory

    // Double free: Freeing the same memory block twice, should prompt a double free error
    free(ptr); 

    // return 0 to end the program
    return 0;
}