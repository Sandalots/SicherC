#include <stdio.h>

// open file with given filename
void openFile(char* filename) {
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
}

