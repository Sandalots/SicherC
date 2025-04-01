# Sicher C Runtime (Sicher.py)
# Sandy MacDonald
# 2003619
# 2025

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

# Sicher Submodules

# Sicher Main Function (Entry Point)
def main():
    # Command Line Arguments
    parser = argparse.ArgumentParser(description='Parse a C source file.')
    parser.add_argument('filename', type=str, help='The C source file to parse')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--gui', action='store_true', help='Run the GUI visualizer')
    parser.add_argument('--output', type=str, help='Output binary filename', default='output_binary')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the input source code filename
    filename = args.filename

    # Tokeniser Module
    with open(filename, 'r') as file:
        # read the source code
        code = file.read()
        
        try:
            # tokenise the source code
            tokens = tokenise(code, debug=args.debug)
            
            # tell the user the tokenisation was successful
            print("\nSource code is lexically correct\n")
            
        # raise a syntax error if there is a problem with the tokenisation
        except SyntaxError as e:
            print(f"Lexical error: {e}")
            sys.exit(1)
    
    # Parser Module
    try:
        # parse the source code
        parse_tokens(tokens, debug=args.debug)
        
        # tell the user the parsing was successful
        print("\nSource code is syntactically correct\n")
        
    # raise a syntax error if there is a problem with the parsing
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)
        
    # Analyser Module
    try:
        # create the AST from the tokens
        ast = create_ast_from_tokens(tokens, debug=args.debug)
        
        # tell the user the AST was created successfully
        print("\nAST created successfully\n")
        
        if args.debug:
            # output the ast prettily
            print(ast.pretty_print())
            
    # raise an error if there is a problem with the AST creation
    except Exception as e:
        print(f"Error creating AST: {e}")
        sys.exit(1)
    
   # Code Generator Module
    try:
        # Run the code generator on the AST
        code_generator = CodeGenerator(ast)
        
        # Generate the code
        generated_code = code_generator.generate_code()
        
        # Output the generated code
        print("Generated Code:")
        print(generated_code)
        
        # Save the generated code to a file
        code_generator.save_code_to_file('output.ll')
        
        # Compile the generated code to an ARM64 binary
        code_generator.compile_to_arm64('output.ll', 'output_binary')
    except Exception as e:
        print(f"Error generating code: {e}")
        sys.exit(1)
    
    # Visualiser Module
    if args.gui:
        try:
            # show the GUI
            visualiser()
            
        # raise an error if there is a problem with the visualiser
        except Exception as e:
            print(f"Error running visualiser: {e}")
            sys.exit(1)

# Run the Sicher (entry point) if run as a script
if __name__ == '__main__':
    main()