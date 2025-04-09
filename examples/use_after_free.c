/* Description: A Simple C Program to create a use after free
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdlib.h>
#include <stdio.h>

int main() {
    // let's create a pointer to an integer
    int* ptr = (int*)malloc(sizeof(int));

    // set the pointer above to have a integer value of 10
    *ptr = 10;

    // free the pointer
    free(ptr);

    // try and use the pointer after it has been freed, thus it is a use after free issue below.
    printf("Value pointed to by ptr: %d\n", *ptr); // Use after free

    // end of the use after free program
    return 0;
}
