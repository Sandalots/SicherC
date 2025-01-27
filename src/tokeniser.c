#include "tokeniser.h"
#include <stdio.h>
#include <stdlib.h>

#define MAX_LINE_LENGTH 255*1024 // debug max-line source file length for the tokeniser to perform on.

const char* TokenTypeStrings[] = {
  "Keyword",
  "Identifier",
  "Literal",
  "Operator",
  "Punctuation",
  "Comment",
  "Whitespace",
  "Preprocessor",
  "Unknown"
};

const char* Keywords[] = {
  "alignas",
  "alignof",
  "auto",
  "bool",
  "break",
  "case",
  "char",
  "const",
  "constexpr",
  "continue",
  "default",
  "do",
  "double",
  "else",
  "enum",
  "extern",
  "false",
  "float",
  "for",
  "goto",
  "if",
  "inline",
  "int",
  "long",
  "nullptr",
  "register",
  "restrict",
  "return",
  "short",
  "signed",
  "sizeof",
  "static",
  "static_assert",
  "struct",
  "switch",
  "thread_local",
  "true",
  "typedef",
  "typeof",
  "typeof_unqual",
  "union",
  "unsigned",
  "void",
  "volatile",
  "while"
};

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
