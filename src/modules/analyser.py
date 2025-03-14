class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"ASTNode({self.node_type}, {self.value}, {self.children})"

    def pretty_print(self, indent=0):
        value_str = f": {self.value}" if self.value is not None else ""
        result = "  " * indent + f"{self.node_type}{value_str}\n"
        for child in self.children:
            result += child.pretty_print(indent + 1)
        return result

class AST:
    def __init__(self):
        self.root = None

    def set_root(self, root):
        self.root = root

    def __repr__(self):
        return f"AST({self.root})"

    def pretty_print(self):
        if self.root:
            return self.root.pretty_print()
        else:
            return "Empty AST"

def create_ast_from_tokens(tokens, debug=False):
    ast = AST()
    current_node = None
    stack = []

    for token in tokens:
        token_type, token_value = token
        if debug:
            print(f"Processing token: {token_type}, {token_value}")

        if token_type == 'KEYWORD':
            if token_value == 'int':
                if current_node is None:
                    current_node = ASTNode("Function", "main")
                    ast.set_root(current_node)
                    block_node = ASTNode("Block")
                    current_node.add_child(block_node)
                    stack.append(current_node)
                    current_node = block_node
                else:
                    var_node = ASTNode("VariableDeclaration", token_value)
                    current_node.add_child(var_node)
                    stack.append(current_node)
                    current_node = var_node
            elif token_value == 'return':
                return_node = ASTNode("Return")
                current_node.add_child(return_node)
                stack.append(current_node)
                current_node = return_node
        elif token_type == 'IDENTIFIER':
            if current_node is not None:
                if token_value == 'for':
                    for_node = ASTNode("ForLoop")
                    current_node.add_child(for_node)
                    stack.append(current_node)
                    current_node = for_node
                elif token_value == 'printf':
                    func_call_node = ASTNode("FunctionCall", token_value)
                    current_node.add_child(func_call_node)
                    stack.append(current_node)
                    current_node = func_call_node
        elif token_type == 'SYMBOL':
            if token_value == '{':
                block_node = ASTNode("Block")
                current_node.add_child(block_node)
                stack.append(current_node)
                current_node = block_node
            elif token_value == '}':
                current_node = stack.pop()
            elif token_value == '=':
                assign_node = ASTNode("Assignment")
                current_node.add_child(assign_node)
                stack.append(current_node)
                current_node = assign_node
            elif token_value == ';':
                current_node = stack[-1]
                if current_node.node_type == "Return" or current_node.node_type == "FunctionCall":
                    current_node = stack.pop()
            elif token_value == '(':
                if current_node.node_type == "Identifier" and current_node.value == "printf":
                    # Handle function call
                    func_call_node = ASTNode("FunctionCall", current_node.value)
                    current_node = stack.pop()
                    current_node.add_child(func_call_node)
                    stack.append(current_node)
                    current_node = func_call_node
            elif token_value == '[':
                array_access_node = ASTNode("ArrayAccess", current_node.children[-1].value)
                current_node.children[-1] = array_access_node
                stack.append(current_node)
                current_node = array_access_node
            elif token_value == ']':
                current_node = stack.pop()
            elif token_value == '<':
                condition_node = ASTNode("Condition")
                current_node.add_child(condition_node)
                stack.append(current_node)
                current_node = condition_node
                operator_node = ASTNode("Operator", token_value)
                current_node.add_child(operator_node)
            elif token_value == '++':
                increment_node = ASTNode("Increment")
                current_node.add_child(increment_node)
                stack.append(current_node)
                current_node = increment_node
                operator_node = ASTNode("Operator", token_value)
                current_node.add_child(operator_node)
        elif token_type == 'STRING':
            string_node = ASTNode("String", token_value)
            current_node.add_child(string_node)
        elif token_type == 'NUMBER':
            number_node = ASTNode("Number", token_value)
            current_node.add_child(number_node)

    return ast