from tokeniser import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def parse(self):
        while self.current_token < len(self.tokens):
            token_type, token_value = self.tokens[self.current_token]
            if token_type == 'KEYWORD' and token_value == 'int':
                self.parse_function()
            else:
                self.current_token += 1

    def parse_function(self):
        self.expect('KEYWORD', 'int')
        self.expect('IDENTIFIER')
        self.expect('SYMBOL', '(')
        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', '{')
        while self.tokens[self.current_token][1] != '}':
            self.current_token += 1
        self.expect('SYMBOL', '}')

    def expect(self, token_type, token_value=None):
        if self.current_token >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        token = self.tokens[self.current_token]
        if token[0] != token_type or (token_value and token[1] != token_value):
            raise SyntaxError(f"Expected {token_type} {token_value}, got {token}")
        self.current_token += 1

def parse_code(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    parser.parse()