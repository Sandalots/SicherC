#include "tokeniser.h"
#include "parser.h"
#include "analyser.h"
#include "code_generator.h"
#include "compiler_fabric.h"

#include <stdio.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    char* filename = argv[1];
    writeContents(filename); 

    return 0;
}
  // parse into ast

  // declarations/ type / memory safety

  // output memory safe code
