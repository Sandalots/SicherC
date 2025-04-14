/* Description: A Simple C Program to create a use after free
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdlib.h>
#include <stdio.h>

int main() {
    // the temp value to be passed to the pointer
    int value = 77; // the value of the integer

    // set the pointer above to have a integer value of 10
    int* ptr = &value; // create a pointer to the integer value

    // free the pointer
    free(ptr);

    // try and use the pointer after it has been freed, thus it is a use after free issue below.
    printf("Value pointed to by ptr: %d\n", *ptr); // Use after free

    // end of the use after free program
    return 0;
}
