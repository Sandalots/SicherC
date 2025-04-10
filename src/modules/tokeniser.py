# Tokeniser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Tokeniser Module Dependencies
import re # for matching regular expressions
import sys # for checking if the user is running in debug mode
import io # for capturing the debug output and redirecting the output so the visualiser can see and read it

# Defining C keywords and symbols
keywords = {'int', 'char', 'return', 'printf', 'strcpy', 'malloc', 'sizeof', 'free', 'if', 'else', 'for', 'while', 'do', 'break', 'continue'} # the keywords Sicher will be able to recognise in given C source files
symbols = {'(', ')', '{', '}', '[', ']', ';', ',', '=', '!', '?', ':', '%', '\\', '&', '*', '+', '-', '/', '<', '>', '==', '!=', '<=', '>=', '&&', '||', '++', '--'} # the symbols/punctuation Sicher will be able to recognise in given C source files

# C Token Types
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
IDENTIFIER = 'IDENTIFIER'
NUMBER = 'NUMBER'
STRING = 'STRING'
COMMENT = 'COMMENT'
PREPROCESSOR = 'PREPROCESSOR'
UNKNOWN = 'UNKNOWN'

# Method to tokenise a given c source file
def tokenise(code, debug=False):
    """
    Tokenises the given C code.

    Args:
        code (str): The C source code to tokenise.
        debug (bool): Whether to include debug logs.

    Returns:
        tuple: A tuple containing the list of tokens and the debug output as a string.
    """
    
    # create a empty list to store the eventual tokens
    tokens = []

    # Redirect stdout to capture debug output
    if debug:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

    try:
        # Remove any comments from source code
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        if debug:
            print("Removed comments from the source code.")

        # Handle string literals
        string_literals = re.findall(r'"(.*?)"', code)
        
        for string_literal in string_literals:
            code = code.replace(f'"{string_literal}"', 'STRING_LITERAL_PLACEHOLDER', 1)
            
        if debug:
            print("Handled string literals:", string_literals)

        lines = code.split('\n')
        for line_number, line in enumerate(lines, start=1):
            # Handle preprocessor directives
            if line.startswith('#'):
                tokens.append((PREPROCESSOR, line.strip()))
                
                if debug:
                    print(f"Line {line_number}: Found preprocessor directive: {line.strip()}")
                    
                continue

            # Remove single-line comments
            line = re.sub(r'//.*', '', line)

            # Tokenize the line
            words = re.findall(r'\w+|[^\s\w]', line)
            for word in words:
                if word == 'STRING_LITERAL_PLACEHOLDER':
                    tokens.append((STRING, string_literals.pop(0)))
                    if debug:
                        print(f"Line {line_number}: Found string literal.")
                elif word in keywords:
                    tokens.append((KEYWORD, word))
                    if debug:
                        print(f"Line {line_number}: Found keyword: {word}")
                elif word in symbols:
                    tokens.append((SYMBOL, word))
                    if debug:
                        print(f"Line {line_number}: Found symbol: {word}")
                elif re.match(r'^[0-9]+$', word):
                    tokens.append((NUMBER, word))
                    if debug:
                        print(f"Line {line_number}: Found number: {word}")
                elif re.match(r'^[a-zA-Z_]\w*$', word):
                    tokens.append((IDENTIFIER, word))
                    if debug:
                        print(f"Line {line_number}: Found identifier: {word}")
                else:
                    tokens.append((UNKNOWN, word))
                    if debug:
                        print(f"Line {line_number}: Found unknown token: {word}")

        # if the tokenisation has completed without error, tell the user the Tokeniser has completed its work
        if debug:
            print("Tokenisation complete.")

        # Capture the debug output
        if debug:
            # define the debug output
            debug_output = sys.stdout.getvalue()

    finally:
        # Restore original stdout
        if debug:
            sys.stdout = old_stdout

    # Returns the list of tokens the tokeniser has generated, and the debug workings if we are in debug mode either just set an empty debug outpput
    return tokens, debug_output if debug else ""