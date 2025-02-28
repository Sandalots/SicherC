// a use after free example of a memory vulnerability c program
#include <stdlib.h>
#include <stdio.h>

int main() {
    int* ptr = (int*)malloc(sizeof(int));
    *ptr = 10;
    free(ptr);
    printf("Value pointed to by ptr: %d\n", *ptr); // Use after free
    return 0;
}
