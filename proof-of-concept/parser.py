class Parser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.current_token = 0
        self.debug = debug

    def parse(self):
        while self.current_token < len(self.tokens):
            token_type, token_value = self.tokens[self.current_token]
            if self.debug:
                print(f"Parsing token: {token_type}, {token_value}")
            if token_type == 'KEYWORD' and token_value == 'int':
                self.parse_function()
            else:
                self.current_token += 1

    def parse_function(self):
        if self.debug:
            print("Parsing function")
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
            print(f"Parsing statement: {token_type}, {token_value}")
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
            print("Parsing return statement")
        self.expect('KEYWORD', 'return')
        self.expect('NUMBER')
        self.expect('SYMBOL', ';')

    def parse_declaration(self):
        if self.debug:
            print("Parsing declaration")
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
                else:
                    self.expect('IDENTIFIER')
            if self.tokens[self.current_token][1] == ',':
                self.expect('SYMBOL', ',')
            else:
                break
        self.expect('SYMBOL', ';')
        if self.debug:
            print(f"Declared variable: {identifier}")

    def parse_expression(self):
        if self.debug:
            print("Parsing expression")
        if self.tokens[self.current_token][1] == '*':
            self.expect('SYMBOL', '*')
        identifier = self.expect('IDENTIFIER')
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
        self.expect('SYMBOL', ';')
        if self.debug:
            print(f"Function call: {identifier}")

    def parse_if(self):
        if self.debug:
            print("Parsing if statement")
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
            print("Parsing for loop")
        self.expect('IDENTIFIER', 'for')
        self.expect('SYMBOL', '(')
        self.parse_declaration()  # Handle the initialization part
        self.expect('SYMBOL', ';')
        self.parse_expression()  # Handle the condition part
        self.expect('SYMBOL', ';')
        self.parse_expression()  # Handle the increment part
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        while self.tokens[self.current_token][1] != '}':
            self.parse_statement()
        self.expect('SYMBOL', '}')

    def expect(self, token_type, token_value=None):
        if self.current_token >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        token = self.tokens[self.current_token]
        if token[0] != token_type or (token_value is not None and token[1] != token_value):
            raise SyntaxError(f"Expected {token_type} {token_value}, got {token}")
        if self.debug:
            print(f"Matched {token_type} {token[1]}")
        self.current_token += 1
        return token[1]

def parse_tokens(tokens, debug=False):
    parser = Parser(tokens, debug=debug)
    parser.parse()