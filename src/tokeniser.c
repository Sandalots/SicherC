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

    // ... (Tokenization logic here) 

    fclose(fp);
    return token; // Return the identified token
}
