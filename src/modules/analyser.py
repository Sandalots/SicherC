class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class AST:
    def __init__(self):
        self.root = None

    def set_root(self, root):
        self.root = root

    def pretty_print(self, node=None, indent=0):
        """
        Recursively prints the AST in a readable format.
        """
        if node is None:
            node = self.root

        if node is not None:
            print("  " * indent + f"{node.node_type}: {node.value if node.value else ''}")
            for child in node.children:
                self.pretty_print(child, indent + 1)


def create_ast_from_tokens(tokens, debug=False):
    ast = AST()
    current_node = None
    stack = []

    for token in tokens:
        token_type, token_value = token

        if debug:
            print(f"Processing token: {token_type}, {token_value}")

        if token_type == "KEYWORD":
            if token_value == "int":
                if current_node is None:
                    # Create the root function node
                    current_node = ASTNode("Function", "main")
                    ast.set_root(current_node)
                    block_node = ASTNode("Block")
                    current_node.add_child(block_node)
                    stack.append(current_node)
                    current_node = block_node
                else:
                    # Create a variable declaration node
                    var_decl_node = ASTNode("VariableDeclaration", "int")
                    current_node.add_child(var_decl_node)
                    stack.append(current_node)
                    current_node = var_decl_node

            elif token_value == "return":
                return_node = ASTNode("Return")
                current_node.add_child(return_node)
                stack.append(current_node)
                current_node = return_node

            elif token_value == "printf":
                func_call_node = ASTNode("FunctionCall", token_value)
                current_node.add_child(func_call_node)
                stack.append(current_node)
                current_node = func_call_node

        elif token_type == "IDENTIFIER":
            id_node = ASTNode("Identifier", token_value)
            current_node.add_child(id_node)

        elif token_type == "SYMBOL":
            if token_value == "{":
                block_node = ASTNode("Block")
                current_node.add_child(block_node)
                stack.append(current_node)
                current_node = block_node

            elif token_value == "}":
                current_node = stack.pop()

            elif token_value == "=":
                assign_node = ASTNode("Assignment")
                current_node.add_child(assign_node)
                stack.append(current_node)
                current_node = assign_node

            elif token_value == "+":
                binary_op_node = ASTNode("BinaryOp", "+")
                current_node.add_child(binary_op_node)
                stack.append(current_node)
                current_node = binary_op_node

            elif token_value == ";":
                current_node = stack[-1]
                if current_node.node_type in ["Return", "FunctionCall", "Assignment", "BinaryOp"]:
                    current_node = stack.pop()

        elif token_type == "STRING":
            string_node = ASTNode("String", token_value)
            current_node.add_child(string_node)

        elif token_type == "NUMBER":
            number_node = ASTNode("Number", int(token_value))
            current_node.add_child(number_node)
            
    # Applying submodules for memory safety

    return ast

# def apply_memory_safety_measures(ast):
#     """
#     Applies memory safety measures to the AST using submodules.
#     """
#     if ast.root:
#         # Apply each submodule to the AST
#         resize_array(ast)
#         remove_unused(ast)
#         prevent_use_after_free(ast)
#         prevent_double_free(ast)
#         remove_dangling_pointers(ast)