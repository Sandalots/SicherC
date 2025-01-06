// token.h
#ifndef TOKEN_H
#define TOKEN_H

typedef enum {
    TOKEN_TYPE_UNKNOWN,
    TOKEN_TYPE_IDENTIFIER,
    TOKEN_TYPE_KEYWORD,
    TOKEN_TYPE_OPERATOR,
    TOKEN_TYPE_INTEGER_LITERAL,
    TOKEN_TYPE_FLOAT_LITERAL,
    TOKEN_TYPE_STRING_LITERAL,
    TOKEN_TYPE_COMMENT,
    TOKEN_TYPE_PREPROCESSOR_DIRECTIVE,
    TOKEN_TYPE_SEPARATOR,
    TOKEN_TYPE_FUNCTION_DECLARATION,
    TOKEN_TYPE_FUNCTION_DEFINITION
} TokenType;

typedef struct {
    TokenType type;
    char value[256];
} Token;

#endif

// tokeniser.h
#ifndef TOKENISER_H
#define TOKENISER_H

#include "token.h" 

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

#endif
