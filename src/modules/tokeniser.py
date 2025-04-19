# Tokeniser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Tokeniser Module Dependencies
import re  # for matching regular expressions
import sys  # for checking if the user is running in debug mode
import io  # for capturing the debug output and redirecting the output so the visualiser can see and read it

# Defining C keywords and symbols for Sicher 
keywords = {'int', 'char', 'return', 'printf', 'strcpy', 'malloc', 'sizeof', 'free', 'if', 'else', 'for', 'while', 'do', 'break', 'continue'}  # the keywords Sicher will be able to recognise in given C source files
symbols = {'(', ')', '{', '}', '[', ']', ';', ',', '=', '!', '?', ':', '%', '\\', '&', '*', '+', '-', '/', '<', '>', '==', '!=', '<=', '>=', '&&', '||', '++', '--'}  # the symbols/punctuation Sicher will be able to recognise in given C source files

# Sicher C Token Types
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
IDENTIFIER = 'IDENTIFIER'
NUMBER = 'NUMBER'
STRING = 'STRING'
COMMENT = 'COMMENT'
PREPROCESSOR = 'PREPROCESSOR'
UNKNOWN = 'UNKNOWN'

# Turns an input c source file into a collectino of sicher created tokens
def tokenise(code, debug=False):
    """
    Tokenises the given C code.

    Args:
        code (str): The C source code to tokenise.
        debug (bool): Whether to include debug logs.

    Returns:
        tuple: A tuple containing the list of tokens and the debug output as a string.
    """
    
    # Collects any tokens from the input c source file
    tokens = []

    # if user requires debug flag in the entry point, collect all logging and printing from the tokeniser
    if debug:
        old_stdout = sys.stdout # defines the old standard output
        sys.stdout = io.StringIO() # redirect stdout to a string version

    try:
        # Remove any comments from source code
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # tell the user comments have been removed
        if debug:
            print("Removed comments from the source code.")

        # find any string leterals
        string_literals = re.findall(r'"(.*?)"', code)
        
        # handle the string literals
        for string_literal in string_literals:
            # give any string literal a placeholder string literal token, to be replaced later
            code = code.replace(f'"{string_literal}"', 'STRING_LITERAL_PLACEHOLDER', 1)
            
        # tell the user string literals have been handled
        if debug:
            print("Handled string literals:", string_literals)

        # Split the code into lines
        lines = code.split('\n')
        
        # process each line in the source code
        for line_number, line in enumerate(lines, start=1): # starts at line 1
            
            # Handle preprocessors
            if line.startswith('#'):
                # tokenise any preprocessor directives
                tokens.append((PREPROCESSOR, line.strip()))
                
                # if the debug flag is set, print the line of where sicher tokensied the pre-procesor token
                if debug:
                    print(f"Line {line_number}: Found preprocessor directive: {line.strip()}")
                    
                # contine to the next line
                continue

            # Remove single-line comments
            line = re.sub(r'//.*', '', line)

            # get the words from the line
            words = re.findall(r'\w+|[^\s\w]', line)
            
            # for all the words on the current line
            for word in words:
                # if the current word is the above created string literal placeholder
                if word == 'STRING_LITERAL_PLACEHOLDER':
                    # tokenise as a string and remove from the string literals collection
                    tokens.append((STRING, string_literals.pop(0)))
                    
                    # if the debug flag is set, print the line of where sicher tokensied the string literal
                    if debug:
                        print(f"Line {line_number}: Found string literal.")
                        
                # check if a keyword
                elif word in keywords:
                    # tokenise as a keyword
                    tokens.append((KEYWORD, word))
                    
                    # if the debug flag is set, print the line of where sicher tokensied the keyword
                    if debug:
                        print(f"Line {line_number}: Found keyword: {word}")
                        
                # check if a symbol
                elif word in symbols:
                    # tokenise as a symbol
                    tokens.append((SYMBOL, word))
                    
                    # if the debug flag is set, print the line of where sicher tokensied the symbol
                    if debug:
                        print(f"Line {line_number}: Found symbol: {word}")
                        
                # check if a number
                elif re.match(r'^[0-9]+$', word):
                    # tokenise as a number
                    tokens.append((NUMBER, word))
                    
                    # if the debug flag is set, print the line of where sicher tokensied the number
                    if debug:
                        print(f"Line {line_number}: Found number: {word}")
                        
                # check if an identifier, i.e. a variable name
                elif re.match(r'^[a-zA-Z_]\w*$', word):
                    # tokenise as an identifier
                    tokens.append((IDENTIFIER, word))
                    
                    # if the debug flag is set, print the line of where sicher tokensied the identifier
                    if debug:
                        print(f"Line {line_number}: Found identifier: {word}")
                     
                # handle unknown tokens   
                else:
                    # tokenise as an unknown token
                    tokens.append((UNKNOWN, word))
                    
                    # if the debug flag is set, print the line of where sicher tokensied the unknown token
                    if debug:
                        print(f"Line {line_number}: Found unknown token: {word}")

            # Check if the line ends with a valid token, i.e end of line validation
            if words:
                last_token = words[-1] # get the last token in the line
                
                # check if the last token is properly terminated with either (';', '{', '}' or '>')
                if last_token not in {';', '{', '}', '>'}:
                    
                    # raise a syntax error along with the line, and where the expected terminating symbol should be on the what token
                    raise SyntaxError(
                        f"Line {line_number}: Invalid line ending. Expected one of ';', '{{', '}}', or '>', "
                        f"but got '{last_token}'."
                    )

        # If the tokenisation has completed without error, tell the user the Tokeniser has completed its work
        if debug:
            print("Tokenisation complete.")

        # Capture the debug output
        if debug:
            # Define the debug output
            debug_output = sys.stdout.getvalue()
    
    # after tokenisation is complete I need to set the stdout to be the old stream so the visualiser can see an access the logs from there
    finally:
        # Restore original stdout if debug flag is set
        if debug:
            # set the standard output back to the original standard output
            sys.stdout = old_stdout

    # Returns the list of tokens the tokeniser has generated, and the debug workings if we are in debug mode either just set an empty debug output
    return tokens, debug_output if debug else ""