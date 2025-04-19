/* Description: A Simple C Program to create a dangling pointer
*  Author: Sandalots
*  Date: 12/03/2025 */

// use the standard io library
#include <stdio.h>

// main method to create a dangling pointer
int main() {
    // define the dangling pointer
    int local_var = 10; // local variable
    int* dangling_ptr = &local_var; // create a pointer to the local variable

    // This will likely lead to undefined behavior, as local_var is no longer valid
    printf("Value pointed to by dangling pointer: %d\n", *dangling_ptr); 

    // end the program
    return 0;
}