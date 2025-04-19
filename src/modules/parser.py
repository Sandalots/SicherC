# Parser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Parser Module Dependencies
import io # for allowing the visualiser to see the debug output
import sys # checking if we are in debug mode, client can also not be in debug mode

# Class to model the Sicher Parser
class Parser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens # the list of tokens from the tokeniser to parse
        self.current_token = 0 # the current token index sicher is parsing
        self.debug = debug # the debug flag, to provide additional logging

    # The parse function to parse the list of tokens
    def parse(self):
        # while there are still tokens to parse
        while self.current_token < len(self.tokens):
            # get the current token type and value
            token_type, token_value = self.tokens[self.current_token]
            
            # if debug flag is set output the current line number, token type and value
            if self.debug:
                print(f"Line {self.current_token + 1}: Parsing token: {token_type}, {token_value}")
            
            # check if the current token is a keyword and if it is an int
            if token_type == 'KEYWORD' and token_value == 'int':
                # parse the function
                self.parse_function()
                
            # increment the current token index
            else:
                self.current_token += 1

    # parse rule for a function
    def parse_function(self):
        # output line number and token if debug flag is set
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing function")
            
        # Function parse rule
        self.expect('KEYWORD', 'int') # expects the int keyword
        self.expect('IDENTIFIER') # expects the function name
        self.expect('SYMBOL', '(') # expects the opening parenthesis
        self.expect('SYMBOL', ')') # expects the closing parenthesis
        self.expect('SYMBOL', '{') # expects the opening brace
        
        # parse rule for statements in the function
        while self.tokens[self.current_token][1] != '}':
            self.parse_statement()
            
        # expect a ending brace/parenthesis
        self.expect('SYMBOL', '}')

    # parse rule for statements
    def parse_statement(self):
        # get the current token type and value
        token_type, token_value = self.tokens[self.current_token]
        
        # if debug flag is set output the current line number, token type and value
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing statement: {token_type}, {token_value}")
            
        if token_type == 'KEYWORD' and token_value == 'return':
            self.parse_return()
            
        elif token_type == 'KEYWORD' and token_value in {'char', 'int'}:
            self.parse_declaration()
            
        elif token_type == 'KEYWORD' and token_value == 'if':
            self.parse_if()
            
        elif token_type == 'IDENTIFIER' and token_value == 'for':
            self.parse_for()
            
        elif token_type == 'IDENTIFIER' or (token_type == 'SYMBOL' and token_value == '*'):
            self.parse_expression()
            
        else:
            self.current_token += 1

    # parse rule for returns
    def parse_return(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing return statement")
            
        self.expect('KEYWORD', 'return')
        
        if self.tokens[self.current_token][1] == '&':
            self.expect('SYMBOL', '&')  # Handle the address-of operator
            self.expect('IDENTIFIER')  # Expect a variable name
            
        else:
            self.expect('NUMBER')  # Handle returning a number
            
        self.expect('SYMBOL', ';')

    # parse rule for declarations
    def parse_declaration(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing declaration")
            
        self.expect('KEYWORD')  # Expect a type like 'int'
        
        while True:
            if self.tokens[self.current_token][1] == '*':
                self.expect('SYMBOL', '*')  # Handle pointer declaration
                
            identifier = self.expect('IDENTIFIER')  # Expect a variable name
            
            if self.tokens[self.current_token][1] == '[':
                self.expect('SYMBOL', '[')
                self.expect('NUMBER')  # Expect array size
                self.expect('SYMBOL', ']')
                
            if self.tokens[self.current_token][1] == '=':
                self.expect('SYMBOL', '=')  # Handle initialization
                self.parse_expression()  # Parse the expression after '='
                
            if self.tokens[self.current_token][1] == ',':
                self.expect('SYMBOL', ',')  # Handle multiple declarations
                
            else:
                break
            
        self.expect('SYMBOL', ';')  # Expect the semicolon at the end
        
        if self.debug:
            print(f"Line {self.current_token + 1}: Declared variable: {identifier}")
            
    # parse rule for expressions
    def parse_expression(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing expression")
            
        if self.tokens[self.current_token][1] in {'&', '*'}:
            operator = self.expect('SYMBOL')  # Handle address-of or dereference operator
            
            if self.debug:
                print(f"Line {self.current_token + 1}: Found operator: {operator}")
        
        self.parse_term()  # Parse the first term
        
        while self.tokens[self.current_token][1] in {'+', '-', '*', '/'}:
            operator = self.expect('SYMBOL')  # Expect a binary operator
            
            if self.debug:
                print(f"Line {self.current_token + 1}: Found operator: {operator}")
                
            self.parse_term()  # Parse the next term

    # parse rule for terms
    def parse_term(self):
        token_type, token_value = self.tokens[self.current_token]
        
        if token_type == 'IDENTIFIER':
            self.expect('IDENTIFIER')  # Handle variables
            
            if self.tokens[self.current_token][1] == '[':
                self.expect('SYMBOL', '[')  # Handle array indexing
                self.parse_expression()  # Parse the index expression
                self.expect('SYMBOL', ']')
                
        elif token_type == 'NUMBER':
            self.expect('NUMBER')  # Handle numbers
            
        elif token_type == 'SYMBOL' and token_value == '(':
            self.expect('SYMBOL', '(')  # Handle parentheses
            self.parse_expression()  # Parse the expression inside parentheses
            self.expect('SYMBOL', ')')
            
        else:
            raise SyntaxError(f"Line {self.current_token + 1}: Unexpected token: {token_type} {token_value}")

    # parse rule for expects
    def expect(self, token_type, token_value=None):
        if self.current_token >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        
        token = self.tokens[self.current_token]
        
        if token[0] != token_type or (token_value is not None and token[1] != token_value):
            raise SyntaxError(f"Line {self.current_token + 1}: Expected {token_type} {token_value}, got {token}")
        
        if self.debug:
            print(f"Line {self.current_token + 1}: Matched {token_type} {token[1]}")
            
        self.current_token += 1
        
        return token[1]

# the main function, parse_tokens to parse tokens from the tokeniser and optional additional debug output
def parse_tokens(tokens, debug=False):
    """
    Parses the tokens and optionally returns debug output.

    Args:
        tokens: The list of tokens to parse.
        debug: Whether to enable debug mode.

    Returns:
        str: The debug output if debug=True, otherwise an empty string.
    """
    # define the parse, passing the tokens and debug flag
    parser = Parser(tokens, debug=debug)
    
    # if debug flag is set, return the debug output
    if debug:
        # Redirect stdout to capture debug output
        old_stdout = sys.stdout # Save the original stdout
        sys.stdout = io.StringIO() # redirect old output to a string buffer so the visualiser can access it
        
        # attempt to parse the tokens and capture the debug output
        try:
            parser.parse() # parse the tokens
            debug_output = sys.stdout.getvalue() # Capture the debug output
            
        # if sicher can parse the tokens, next step is to revert the stdout for the visualiser to see the log
        finally:
            sys.stdout = old_stdout  # Restore original stdout
            
        # return the debug output
        return debug_output
    
    # if debug flag is not set
    else:
        # apply the parser to the tokens
        parser.parse()
        
        # return an empty string to account for the no debug flag
        return ""