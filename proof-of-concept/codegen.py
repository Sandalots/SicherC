from typing import List

class Instruction:
    def __init__(self, op: str, args: List[str]):
        self.op = op
        self.args = args

    def __str__(self):
        return f"{self.op} {' '.join(self.args)}"

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

def tokenize(code):
    tokens = []
    for char in code:
        if char.isalpha():
            tokens.append(Token('ID', char))
        elif char.isdigit():
            tokens.append(Token('NUM', char))
        elif char in ['+', '-', '*', '/', '=', ';', '(', ')']:
            tokens.append(Token(char, char))
    tokens.append(Token('EOF', None))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current += 1
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")

    def peek(self):
        return self.tokens[self.current]

    def parse(self):
        return self.expr()

    def expr(self):
        result = self.term()
        while self.current_token.type in ['+', '-']:
            op = self.current_token
            self.eat(op.type)
            right = self.term()
            result = Instruction('binop', [result, op.value, right])
        return result

    def term(self):
        result = self.factor()
        while self.current_token.type in ['*', '/']:
            op = self.current_token
            self.eat(op.type)
            right = self.factor()
            result = Instruction('binop', [result, op.value, right])
        return result

    def factor(self):
        if self.current_token.type == '(':
            self.eat('(')
            result = self.expr()
            self.eat(')')
            return result
        elif self.current_token.type == 'NUM':
            result = Instruction('const', [self.current_token.value])
            self.eat('NUM')
            return result
        elif self.current_token.type == 'ID':
            result = Instruction('id', [self.current_token.value])
            self.eat('ID')
            return result
        else:
            raise Exception("Invalid syntax")

    @property
    def current_token(self):
        return self.tokens[self.current]

def compile(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    return str(ast)

if __name__ == "__main__":
    code = "a = 1 + 2;" 
    ir = compile(code)
    print(ir)  # Output: binop [const 1 + const 2]
