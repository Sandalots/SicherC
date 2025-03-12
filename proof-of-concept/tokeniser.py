import re
import argparse

# Define the keywords and symbols
keywords = {'int', 'char', 'return', 'printf', 'strcpy', 'malloc', 'sizeof', 'free'}
symbols = {'(', ')', '{', '}', '[', ']', ';', ',', '=', '!', '?', ':', '%', '\\', '&', '*'}

# Token types
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
IDENTIFIER = 'IDENTIFIER'
NUMBER = 'NUMBER'
STRING = 'STRING'
COMMENT = 'COMMENT'
PREPROCESSOR = 'PREPROCESSOR'
UNKNOWN = 'UNKNOWN'

def tokenize(code, debug=False):
    tokens = []
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    if debug:
        print("Removed multi-line comments")
    # Handle string literals
    string_literals = re.findall(r'"(.*?)"', code)
    for string_literal in string_literals:
        code = code.replace(f'"{string_literal}"', 'STRING_LITERAL_PLACEHOLDER', 1)
    if debug:
        print("Handled string literals:", string_literals)
    lines = code.split('\n')
    for line in lines:
        # Handle preprocessor directives
        if line.startswith('#'):
            tokens.append((PREPROCESSOR, line.strip()))
            if debug:
                print("Found preprocessor directive:", line.strip())
            continue
        # Remove single-line comments
        line = re.sub(r'//.*', '', line)
        # Tokenize the line
        words = re.findall(r'\w+|[^\s\w]', line)
        for word in words:
            if word == 'STRING_LITERAL_PLACEHOLDER':
                tokens.append((STRING, string_literals.pop(0)))
                if debug:
                    print("Found string literal")
            elif word in keywords:
                tokens.append((KEYWORD, word))
                if debug:
                    print("Found keyword:", word)
            elif word in symbols:
                tokens.append((SYMBOL, word))
                if debug:
                    print("Found symbol:", word)
            elif re.match(r'^[0-9]+$', word):
                tokens.append((NUMBER, word))
                if debug:
                    print("Found number:", word)
            elif re.match(r'^[a-zA-Z_]\w*$', word):
                tokens.append((IDENTIFIER, word))
                if debug:
                    print("Found identifier:", word)
            else:
                tokens.append((UNKNOWN, word))
                if debug:
                    print("Found unknown token:", word)
    return tokens

def main():
    parser = argparse.ArgumentParser(description='Tokenize a C source file.')
    parser.add_argument('filename', type=str, help='The C source file to tokenize')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    # Read the C source file
    with open(args.filename, 'r') as file:
        code = file.read()

    # Tokenize the code
    tokens = tokenize(code, debug=args.debug)

    # Print the tokens
    for token in tokens:
        print(token)

if __name__ == '__main__':
    main()