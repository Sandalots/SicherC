#include <stdio.h>

int* create_dangling_pointer() {
    int local_var = 10;
    return &local_var; // Returning the address of a local variable
}

int main() {
    int* dangling_ptr = create_dangling_pointer();

    // This will likely lead to undefined behavior, as local_var is no longer valid
    printf("Value pointed to by dangling pointer: %d\n", *dangling_ptr); 

    return 0;
}