# Parser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Parser Module Dependencies
import io
import sys

# Class to model the Sicher Parser
class Parser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.current_token = 0
        self.debug = debug

    def parse(self):
        while self.current_token < len(self.tokens):
            token_type, token_value = self.tokens[self.current_token]
            if self.debug:
                print(f"Line {self.current_token + 1}: Parsing token: {token_type}, {token_value}")
            if token_type == 'KEYWORD' and token_value == 'int':
                self.parse_function()
            else:
                self.current_token += 1

    def parse_function(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing function")
        self.expect('KEYWORD', 'int')
        self.expect('IDENTIFIER')
        self.expect('SYMBOL', '(')
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        while self.tokens[self.current_token][1] != '}':
            self.parse_statement()
        self.expect('SYMBOL', '}')

    def parse_statement(self):
        token_type, token_value = self.tokens[self.current_token]
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

    def parse_return(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing return statement")
        self.expect('KEYWORD', 'return')
        self.expect('NUMBER')
        self.expect('SYMBOL', ';')

    def parse_declaration(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing declaration")
        self.expect('KEYWORD')
        while True:
            if self.tokens[self.current_token][1] == '*':
                self.expect('SYMBOL', '*')
            identifier = self.expect('IDENTIFIER')
            if self.tokens[self.current_token][1] == '[':
                self.expect('SYMBOL', '[')
                self.expect('NUMBER')
                self.expect('SYMBOL', ']')
            if self.tokens[self.current_token][1] == '=':
                self.expect('SYMBOL', '=')
                if self.tokens[self.current_token][0] == 'STRING':
                    self.expect('STRING')
                elif self.tokens[self.current_token][0] == 'NUMBER':
                    self.expect('NUMBER')
                else:
                    self.expect('IDENTIFIER')
            if self.tokens[self.current_token][1] == ',':
                self.expect('SYMBOL', ',')
            else:
                break
        self.expect('SYMBOL', ';')
        if self.debug:
            print(f"Line {self.current_token + 1}: Declared variable: {identifier}")

    def parse_expression(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing expression")
        if self.tokens[self.current_token][1] == '*':
            self.expect('SYMBOL', '*')
        identifier = self.expect('IDENTIFIER')
        if self.tokens[self.current_token][1] == '(':
            self.expect('SYMBOL', '(')
            while self.tokens[self.current_token][1] != ')':
                if self.tokens[self.current_token][0] == 'IDENTIFIER':
                    self.expect('IDENTIFIER')
                elif self.tokens[self.current_token][0] == 'STRING':
                    self.expect('STRING')
                elif self.tokens[self.current_token][0] == 'NUMBER':
                    self.expect('NUMBER')
                if self.tokens[self.current_token][1] == ',':
                    self.expect('SYMBOL', ',')
            self.expect('SYMBOL', ')')
        else:
            while self.tokens[self.current_token][1] not in {';', ')', ','}:
                if self.tokens[self.current_token][0] == 'IDENTIFIER':
                    self.expect('IDENTIFIER')
                elif self.tokens[self.current_token][0] == 'NUMBER':
                    self.expect('NUMBER')
                elif self.tokens[self.current_token][0] == 'SYMBOL':
                    self.expect('SYMBOL')
        if self.tokens[self.current_token][1] == ';':
            self.expect('SYMBOL', ';')
        if self.debug:
            print(f"Line {self.current_token + 1}: Expression: {identifier}")

    def parse_if(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing if statement")
        self.expect('KEYWORD', 'if')
        self.expect('SYMBOL', '(')
        self.parse_expression()
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        while self.tokens[self.current_token][1] != '}':
            self.parse_statement()
        self.expect('SYMBOL', '}')

    def parse_for(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing for loop")
        self.expect('IDENTIFIER', 'for')
        self.expect('SYMBOL', '(')
        self.parse_for_initialization()  # Handle the initialization part
        self.expect('SYMBOL', ';')
        self.parse_expression()  # Handle the condition part
        self.parse_for_increment()  # Handle the increment part
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        while self.tokens[self.current_token][1] != '}':
            self.parse_statement()
        self.expect('SYMBOL', '}')

    def parse_for_initialization(self):
        token_type, token_value = self.tokens[self.current_token]
        if token_type == 'KEYWORD' and token_value in {'char', 'int'}:
            self.parse_declaration()
        else:
            self.parse_expression()

    def parse_for_increment(self):
        if self.debug:
            print(f"Line {self.current_token + 1}: Parsing for increment")
        while self.tokens[self.current_token][1] != ')':
            self.parse_expression()
            if self.tokens[self.current_token][1] == ',':
                self.expect('SYMBOL', ',')
        if self.debug:
            print(f"Line {self.current_token + 1}: Finished parsing for increment")

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

def parse_tokens(tokens, debug=False):
    """
    Parses the tokens and optionally returns debug output.

    Args:
        tokens: The list of tokens to parse.
        debug: Whether to enable debug mode.

    Returns:
        str: The debug output if debug=True, otherwise an empty string.
    """
    parser = Parser(tokens, debug=debug)
    
    if debug:
        # Redirect stdout to capture debug output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            parser.parse()
            debug_output = sys.stdout.getvalue()  # Capture the debug output
        finally:
            sys.stdout = old_stdout  # Restore original stdout
        return debug_output
    else:
        parser.parse()
        return ""