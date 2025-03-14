# Sicher C Runtime (Sicher.py)
# For my Sicher C Compiler, this is the runtime program that is the mother of all modules, runs the 5 modules sequentially and form which the GUI eventually calls.

# Sicher Dependencies
import sys
import argparse

# Sicher Modules
from modules.tokeniser import tokenise
from modules.parser import parse_tokens
from modules.analyser import create_ast_from_tokens
from modules.visualiser import main as visualiser
from modules.codegenerator import CodeGenerator

def main():
    parser = argparse.ArgumentParser(description='Parse a C source file.')
    parser.add_argument('filename', type=str, help='The C source file to parse')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--gui', action='store_true', help='Run the GUI visualizer')
    parser.add_argument('--output', type=str, help='Output binary filename', default='output_binary')
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
    try:
        ast = create_ast_from_tokens(tokens, debug=args.debug)
        print("AST created successfully\n")
        if args.debug:
            print(ast.pretty_print())
    except Exception as e:
        print(f"Error creating AST: {e}")
        sys.exit(1)
    
    # Code Generator Module
    try:
        code_generator = CodeGenerator(ast)
        generated_code = code_generator.generate_code()
        print("Generated Code:\n")
        print(generated_code)
        
        # Save generated code to a file
        source_filename = 'output.s'
        code_generator.save_code_to_file(source_filename)
        
        # Compile to ARM64 binary
        output_filename = args.output
        code_generator.compile_to_arm64(source_filename, output_filename)
    except Exception as e:
        print(f"Error generating code: {e}")
        sys.exit(1)
    
    # Visualiser Module
    if args.gui:
        try:
            visualiser()
        except Exception as e:
            print(f"Error running visualiser: {e}")
            sys.exit(1)

# Run the Sicher (entry point) if run as a script
if __name__ == '__main__':
    main()