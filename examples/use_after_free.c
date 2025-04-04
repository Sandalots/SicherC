/* Description: A Simple C Program to create a use after free
*  Author: Sandalots
*  Date: 12/03/2025 */

#include <stdlib.h>
#include <stdio.h>

int main() {
    int* ptr = (int*)malloc(sizeof(int));
    *ptr = 10;
    free(ptr);
    printf("Value pointed to by ptr: %d\n", *ptr); // Use after free
    return 0;
}
