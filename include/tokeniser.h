#ifndef TOKENISER_H
#define TOKENISER_H

#include <stdio.h>

#include "token.h" // Include the token.h header

// Function prototypes
Token tokenise(char* filename);
Token tokenise_identifier(char* str);
Token tokenise_keyword(char* str);
Token tokenise_operator(char* str);
Token tokenise_integer_literal(char* str);
Token tokenise_float_literal(char* str);
Token tokenise_string_literal(char* str);
Token tokenise_comment(char* str);
Token tokenise_preprocessor_directive(char* str);
Token tokenise_separator(char* str);

#endif // TOKENIZER_H
