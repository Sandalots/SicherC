import os
from parser import parse_code
import sys
from tokeniser import tokenize

# Get the root directory of the SicherC project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to the source file in the root directory
source_file = os.path.join(root_dir, 'examples/buffer_overflow.c')


def main():
    '''if len(sys.argv) != 2:
        print("Usage: python sicher.py <filename>")
        sys.exit(1)
        '''
    filename = source_file

    # Invoke the tokeniser
    os.system(f'python3 {tokenize} {source_file}')

    # Parser
    with open(filename, 'r') as file:
        code = file.read()
        
        try:
            parse_code(code)
            print("Code is syntactically correct")
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            

if __name__ == '__main__':
    main()