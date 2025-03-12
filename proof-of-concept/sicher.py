import sys
import argparse
from tokeniser import tokenize
from parser import parse_tokens

def main():
    parser = argparse.ArgumentParser(description='Parse a C source file.')
    parser.add_argument('filename', type=str, help='The C source file to parse')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    filename = args.filename

    # Tokenizer
    with open(filename, 'r') as file:
        code = file.read()
        tokens = tokenize(code, debug=args.debug)
    
    # Parser
    try:
        parse_tokens(tokens, debug=args.debug)
        print("Code is syntactically correct")
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()