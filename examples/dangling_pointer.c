/* Description: A Simple C Program to create a dangling pointer
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdio.h>

// A Dangling Pointer Test.
int* create_dangling_pointer() {
    int local_var = 10; // the local variable c
    return &local_var; // Returning the address of a local variable
}

// main method to create a dangling pointer
int main() {
    // define the dangling pointer
    int* dangling_ptr = create_dangling_pointer(); // ceate a dangling pointer

    // This will likely lead to undefined behavior, as local_var is no longer valid
    printf("Value pointed to by dangling pointer: %d\n", *dangling_ptr); 

    // end the program
    return 0;
}