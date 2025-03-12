# Sicher C Runtime (Sicher.py)
# For my Sicher C Compiler, this is the runtime program that is the mother of all modules, runs the 5 modules sequentially and form which the GUI eventually calls.

# Sicher Dependencies
import sys
import argparse
from tokeniser import tokenise
from parser import parse_tokens


def main():
    parser = argparse.ArgumentParser(description='Parse a C source file.')
    parser.add_argument('filename', type=str, help='The C source file to parse')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    filename = args.filename

    # Tokeniser Module
    with open(filename, 'r') as file:
        code = file.read()
        
        try:
            tokens = tokenise(code, debug=args.debug)
            print("Source code is lexically correct\n")
        except SyntaxError as e:
            print(f"Lexical error: {e}")
            sys.exit(1)
    
    # Parser Module
    try:
        parse_tokens(tokens, debug=args.debug)
        print("Source code is syntactically correct\n")
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)
        
    # Analyser Module
    
    # Code Generator Module
    
    # Visualiser Module

if __name__ == '__main__':
    main()