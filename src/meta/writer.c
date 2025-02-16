// method to write to a new file called output.txt

#include <stdio.h>
#include <stdlib.h>


// set filename to be output.txt
char* filename = "output.txt";

// write to file
void writeToFile(char* text) {
    FILE* fp = fopen(filename, "w");

    if (fp == NULL) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        exit(1);
    }

    fprintf(fp, "%s", text);
    fclose(fp);

    printf("File written successfully\n");
}

int main() {
    writeToFile("Hello, World!");
    return 0;
}


