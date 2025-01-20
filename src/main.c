#include "tokeniser.h"
#include "parser.h"
#include "analyser.h"
#include "code_generator.h"
#include "compiler_fabric.h"

#include <stdio.h>

int main(int argc, char* argv[]) {
    // Check if user has given an input source file.
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    // Get filename
    char* filename = argv[1];

    // Tokenise the source file
    writeContents(filename); 


    // parse the tokens

    // analyses the AST

    // Generate hardened memory safe code from the AST


    // output log of changes/countermeasures

    return 0;
}
