#include "tokeniser.h"
#include "file_handling.h"
#include <stdio.h>
#include <stdlib.h>


#define MAX_LINE_LENGTH 255

int tokenise(char* filename) {
    FILE* fp = fopen(filename, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        exit(1);
    }

    int line_count = get_lines(fp);
    printf("Number of lines: %d\n", line_count);

    fclose(fp);
    return line_count; // Return the identified token
}
