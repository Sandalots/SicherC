#include "tokeniser.h"

#include <stdio.h>
#include <stdlib.h>


#define MAX_LINE_LENGTH 255

int writeContents(char* filename) {
    FILE* fp = fopen(filename, "r");
    
    if (fp == NULL) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        exit(1);
    }

    char retrievedff[100];

    while(fgets(retrievedff, 100, fp)) {
      printf("%s", retrievedff);
    }
    
    fclose(fp);
    return 0;
}
