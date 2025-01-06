#include "token.h"
#include "tokeniser.h"
#include "file_handling.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LENGTH 255

Token tokenise(char* filename) {
    FILE* fp = fopen(filename, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        exit(1);
    }

    printf("%d", get_lines(fp));

    fclose(fp);
    return (Token){.type = TOKEN_TYPE_UNKNOWN, .value[0] = '\0'}; 
}
