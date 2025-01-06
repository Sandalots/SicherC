// token.h
#ifndef TOKEN_H
#define TOKEN_H

#include <stdbool.h>

typedef enum {
    TOKEN_TYPE_KEYWORD, 
    TOKEN_TYPE_OPERATOR, 
    TOKEN_TYPE_IDENTIFIER, 
    TOKEN_TYPE_INTEGER_LITERAL, 
    TOKEN_TYPE_FLOAT_LITERAL, 
    TOKEN_TYPE_CHARACTER_LITERAL, 
    TOKEN_TYPE_STRING_LITERAL, 
    TOKEN_TYPE_SEPARATOR, 
    TOKEN_TYPE_PREPROCESSOR, 
    TOKEN_TYPE_COMMENT, 
    TOKEN_TYPE_UNKNOWN 
} TokenType;

typedef struct {
    TokenType type;
    char value[256]; // Adjust size as needed
} Token;

extern const char* keywords[];
extern const char* operators[];
extern const char* separators[];
extern const char* preprocessor_directives[];
extern const char* comment_start[];
extern const char* comment_end[];
extern const char* escape_sequences[];
extern const char* digits[];
extern const char* letters[];

#endif // TOKEN_H

// token.c
const char* keywords[] = {
    "auto", "break", "case", "char", "const", "continue", 
    "default", "do", "double", "else", "enum", "extern", 
    "float", "for", "goto", "if", "int", "long", "register", 
    "return", "short", "signed", "sizeof", "static", "struct", 
    "switch", "typedef", "union", "unsigned", "void", "volatile", 
    "while", "inline", "restrict", "bool", "_Bool", "complex", 
    "_Complex", "imaginary", "_Imaginary", NULL 
};

const char* operators[] = {
    "+", "-", "*", "/", "%", 
    "==", "!=", "<", ">", "<=", ">=", 
    "&&", "||", "!", 
    "=", "+=", "-=", "*=", "/=", "%=", 
    "&", "|", "^", "~", "<<", ">>", 
    "++", "--", 
    ".", "->", 
    "?", ":", 
    sizeof, 
    NULL
};

const char* separators[] = {
    " ", "\t", "\n", ";", ",", 
    "(", ")", "{", "}", "[", "]", 
    ":", "#", 
    NULL
};

const char* preprocessor_directives[] = {
    "#include", "#define", "#ifdef", "#ifndef", "#if", 
    "#else", "#elif", "#endif", "#pragma", "#error", 
    NULL
};

const char* comment_start[] = {
    "/*", 
    "//", 
    NULL
};

const char* comment_end[] = {
    "*/", 
    NULL
};

const char* escape_sequences[] = {
    "\\n", "\\t", "\\r", "\\b", "\\f", "\\v", "\\a", "\\\\", "\\\"", "\\\'", "\\0", 
    NULL
};

const char* digits[] = {
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
    NULL
};

const char* letters[] = {
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
    NULL
};
