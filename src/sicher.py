# Sicher C Runtime (Sicher.py)
# Sandy MacDonald
# 2003619
# 2025

# For my Sicher C Compiler, this is the runtime program that is the mother of all modules, runs the 5 modules sequentially and form which the GUI eventually calls.

# Sicher Dependencies
import sys # for exiting the sicher program
import argparse # for parsing given command line arguments to the sicher program
import os # for checking if the given source code file exists and is a c source code file

# Sicher Modules (The 5 integral modules of the Sicher Compiler)
from modules.tokeniser import tokenise # for tokenising the given c source code
from modules.parser import parse_tokens # for parsing the tokenised c source code
from modules.analyser import create_ast_from_tokens # for modelling the given c source code as an sicher AST
from modules.codegenerator import CodeGenerator # for generating actual assembly code from the AST
from modules.visualiser import main as visualiser # for visualising the AST through the sicher GUI

# Sicher Main Function (Entry Point)
def main():
    """
    Entry Point for my Sicher C Compiler.
    """
    
    # Command Line Arguments for Sicher
    parser = argparse.ArgumentParser(description='Parse a C source file.') # give the parser a description
    parser.add_argument('filename', type=str, help='The C source file to parse') # get the input c source code file
    parser.add_argument('--debug', action='store_true', help='Enable debug output') # get the optional debug flag
    parser.add_argument('--gui', action='store_true', help='Run the GUI visualizer') # get the optional GUI flag
    parser.add_argument('--output', type=str, help='Output binary filename', default='output_binary') # get the oprional output filename
    parser.add_argument('--nocompile', action='store_true', help="Skip the code generation step") # add the --nocompile flag

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the input source code filename
    filename = args.filename
    
    # Check if the source file exists
    try:
        # if sicher can read the given input filename
        with open(filename, 'r') as file:
            # move on to the tokeniser module
            pass
        
    # raise an error if the file does not exist
    except FileNotFoundError:
        # Tell the user the file cannot be found
        print(f"File {filename} not found.")
        
        # exit sicher to prevent additional errors
        sys.exit(1)
        
    # raise an error if the file is not readable
    except IOError:
        # Tell the user there was some issue reading the file and or it is not readable, maybe due to missing permissions?
        print(f"Error reading file {filename}.")
        
        # exit sicher to prevent additional errors
        sys.exit(1)
        
    # Check if the file is empty
    if os.path.getsize(filename) == 0:
        # Tell the user the file is empty and is not valid
        print(f"File {filename} is empty.")
        
        # exit sicher to prevent additional errors
        sys.exit(1)
        
    # Check if the file is a C source file
    if not filename.endswith('.c'):
        # Tell the user the file is not a c source file
        print(f"File {filename} is not a C source file.")
        
        # exit sicher to prevent additional errors
        sys.exit(1)

    # Tokeniser Module
    with open(filename, 'r') as file:
        # read the source code
        code = file.read()
        
        # attempt to tokenise the given c source file
        try:
            # tokenise the source code
            tokens, _ = tokenise(code, debug=args.debug)
            
            # tell the user the tokenisation was successful
            print("\nSource code is lexically correct\n")
            
        # raise a syntax error if there is a problem with the tokenisation
        except SyntaxError as e:
            # prompt the lexical error
            print(f"Lexical error: {e}")
            
            # exit the program to avoid further errors
            sys.exit(1)
    
    # Parser Module
    try:
        # parse the source code
        parse_tokens(tokens, debug=args.debug)
        
        # tell the user the parsing was successful
        print("\nSource code is syntactically correct\n")
        
    # raise a syntax error if there is a problem with the parsing
    except SyntaxError as e:
        # prompt the syntax error
        print(f"Syntax error: {e}")
        
        # exit the program to avoid further errors
        sys.exit(1)
        
    # Analyser Module
    try:
        # create the AST from the tokens
        ast = create_ast_from_tokens(tokens, debug=args.debug)
        
        # tell the user the AST was created successfully
        print("\nAST created successfully\n")
        
        # check if the debug flag is set
        if args.debug:
            # output the ast prettily
            print(ast.pretty_print())
            
    # raise an error if there is a problem with the AST creation
    except Exception as e:
        # prompt the AST creation error
        print(f"Error creating AST: {e}")
        
        # exit the program to avoid further errors
        sys.exit(1)
    
    # Code Generator Module (Skip if --nocompile is set)
    if not args.nocompile:
        try:
            # Run the code generator on the AST
            code_generator = CodeGenerator(ast)
            
            # Generate the code
            generated_code = code_generator.generate_code()
            
            # Output the generated code
            print("Generated Code:")
            
            # the actual generated code
            print(generated_code)
            
            # Save the generated code to a file
            code_generator.save_code_to_file('output.ll')
            
            # Compile the generated code to an ARM64 binary
            code_generator.compile_to_arm64('output.ll', args.output)
        
        # raise an error if there is a problem with the code generation     
        except Exception as e:
            # prompt the code generation error
            print(f"Error generating code: {e}")
            
            # exit the program to avoid further errors
            sys.exit(1)
            
    else:
        # Tell the user the code generation was skipped due to the nocompile flag
        print("\nSkipping code generation as --nocompile flag is set.\n")
    
    # Visualiser Module
    if args.gui:
        # try and show the visualiser/GUI
        try:
            # show the sicher GUI
            visualiser()
            
        # raise an error if there is a problem with the visualiser
        except Exception as e:
            # prompt the visualiser error
            print(f"Error running visualiser: {e}")
            
            # exit the program to avoid further errors
            sys.exit(1)

# Run the Sicher (entry point) if run as a script
if __name__ == '__main__':
    main() # run sicher