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
            # for every statement in the function, parse
            self.parse_statement()
            
        # expect a ending brace
        self.expect('SYMBOL', '}')

    # parse rule for statements
    def parse_statement(self):
        # get the current token type and value
        token_type, token_value = self.tokens[self.current_token]
        
        # if debug flag is set output the current line number, token type and value
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing statement: {token_type}, {token_value}") # debug output
            
        # check if the current token is a keyword and if it is a return statement
        if token_type == 'KEYWORD' and token_value == 'return':
            # parse as a return statement
            self.parse_return()
            
        # check if the current token is a keyword and if it is a a char or int declaration
        elif token_type == 'KEYWORD' and token_value in {'char', 'int'}:
            # parse as a declaration
            self.parse_declaration()
            
        # check if the current token is a keyword and if it is an if statement
        elif token_type == 'KEYWORD' and token_value == 'if':
            # parse as an if statement
            self.parse_if()
            
        # check if the current token is a identifier  and if it is a for statement
        elif token_type == 'IDENTIFIER' and token_value == 'for':
            # parse as a for statement
            self.parse_for()
            
        # check if the current token is a identifier or a symbol and a pointer symbol
        elif token_type == 'IDENTIFIER' or (token_type == 'SYMBOL' and token_value == '*'):
            # parse as an expression
            self.parse_expression()
            
        # if the token doesnt fit any of the above rules increment the current token index
        else:
            # increments the current token index
            self.current_token += 1

    # parse rule for returns
    def parse_return(self):
        # check for debug flag
        if self.debug:
            # output return debug statement
            print(f"Line {self.current_token + 1}: Parsing return statement")
            
        # expect a return keyword
        self.expect('KEYWORD', 'return')
        
        # check for & symbol for pointer dereference
        if self.tokens[self.current_token][1] == '&':
            self.expect('SYMBOL', '&')  # Handle the address-of operator
            self.expect('IDENTIFIER')  # Expect a variable name
            
        # else handle regular number
        else:
            self.expect('NUMBER')  # Handle returning a number
            
        # expect end of line semicolon
        self.expect('SYMBOL', ';')

    # parse rule for declarations
    def parse_declaration(self):
        # check for debug flag
        if self.debug:
            # output declaration debug statement
            print(f"Line {self.current_token + 1}: Parsing declaration")
            
        # expect a keyword for the type
        self.expect('KEYWORD')
        
        # for declarations
        while True:
            # check for pointer symbol
            if self.tokens[self.current_token][1] == '*':
                # expect a pointer symbol
                self.expect('SYMBOL', '*')
                
            # expect an identifier
            identifier = self.expect('IDENTIFIER')
            
            # expect a start of array declaration
            if self.tokens[self.current_token][1] == '[':
                self.expect('SYMBOL', '[') # expect left bracket for start of array
                self.expect('NUMBER')  # Expect array size
                self.expect('SYMBOL', ']') # expect right bracket for end of array
                
            # check for initialization
            if self.tokens[self.current_token][1] == '=':
                self.expect('SYMBOL', '=')  # Handle initialization
                self.parse_expression()  # Parse the expression after '=' symbol
                
            # check for comma for multiple declarations
            if self.tokens[self.current_token][1] == ',':
                self.expect('SYMBOL', ',')  # Handle multiple declarations
               
            # if no more declarations, break 
            else:
                # end the advanced declaration loop
                break
            
        # expect end of line semicolon
        self.expect('SYMBOL', ';')  # Expect the semicolon at the end
        
        # check for debug flag
        if self.debug:
            # output declaration debug statement
            print(f"Line {self.current_token + 1}: Declared variable: {identifier}")
            
    # parse rule for expressions
    def parse_expression(self):
        # check for debug flag
        if self.debug:
            # output expression debug statement
            print(f"Line {self.current_token + 1}: Parsing expression")
            
        # check for pointer dereference or address-of operator
        if self.tokens[self.current_token][1] in {'&', '*'}:
            operator = self.expect('SYMBOL')  # Handle address-of or dereference operator
            
            # check for debug flag
            if self.debug:
                # output expression debug statement
                print(f"Line {self.current_token + 1}: Found operator: {operator}")
        
        # parse the first term
        self.parse_term()
        
        # check for binary operators, the symbols + - * /
        while self.tokens[self.current_token][1] in {'+', '-', '*', '/'}:
            # expect the operator symbol one of the binary operators above
            operator = self.expect('SYMBOL') 
            
            # check for debug flag
            if self.debug:
                # output expression debug statement
                print(f"Line {self.current_token + 1}: Found operator: {operator}")
                
            # parse the next term
            self.parse_term()  # Parse the next term

    # parse rule for terms
    def parse_term(self):
        # get the current token type and value 
        token_type, token_value = self.tokens[self.current_token]
    
        # is the current token a identifer?
        if token_type == 'IDENTIFIER':
            # expect an identifier
            self.expect('IDENTIFIER')  # Handle variables
            
            # handling array indexing
            if self.tokens[self.current_token][1] == '[': # check for array indexing
                self.expect('SYMBOL', '[')  # Handle array indexing
                self.parse_expression()  # Parse the index expression
                self.expect('SYMBOL', ']') # expect a closing array indexing
                
        # is the current token a number?
        elif token_type == 'NUMBER':
            self.expect('NUMBER')  # Handle numbers
            
        # check for expressions, first for a opening parenthesis
        elif token_type == 'SYMBOL' and token_value == '(':
            self.expect('SYMBOL', '(')  # expect a opening parenthesis
            self.parse_expression()  # Parse the expression inside parentheses
            self.expect('SYMBOL', ')') # expect a closing parenthesis
           
        # if there is an issue in the term parsing 
        else:
            # raise a syntax error along with the unexpected token
            raise SyntaxError(f"Line {self.current_token + 1}: Unexpected token: {token_type} {token_value}")

    # parse rule for expects
    def expect(self, token_type, token_value=None):
        # check if the current token is out of bounds
        if self.current_token >= len(self.tokens):
            # raise a syntax error for unexpected end of input
            raise SyntaxError("Unexpected end of input")
        
        # get the current token
        token = self.tokens[self.current_token]
        
        # check if the current token is of the expected type and value
        if token[0] != token_type or (token_value is not None and token[1] != token_value):
            # tell the user there is an unexpected token along with the line number, expected token type and value and the actual token encountered by sicher
            raise SyntaxError(f"Line {self.current_token + 1}: Expected {token_type} {token_value}, got {token}")
        
        # if debug flag is set
        if self.debug:
            # show the user the matched token
            print(f"Line {self.current_token + 1}: Matched {token_type} {token[1]}")
            
        # increment the current token index to move to the next token
        self.current_token += 1
        
        # return the matched token
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