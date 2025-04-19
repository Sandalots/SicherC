# Analyser Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Analyser Module Dependencies

# import the Sicher compile-time Submodules
from submodules.buffer_sizer import resize_array  # buffer sizer submodule
from submodules.unused_remover import remove_unused  # remove unused objects submodule
from submodules.prevent_use_after_free import prevent_use_after_free  # prevent use after free submodule
from submodules.prevent_double_free import prevent_double_free  # prevent double free submodule
from submodules.remove_dangling_pointers import remove_dangling_pointers  # remove dangling pointers submodule

# Encapsulates a child (node) of the AST
class ASTNode:
    # Constructor for ASTNode
    def __init__(self, node_type, value=None): # creates a new node for the ast
        self.node_type = node_type # get the type of the node
        self.value = value # get the value of the node
        self.children = [] # get any children of the current node
        self.parent = None # get the parent of the current noe
        self.isUsed = False  # Flag to indicate if the node is used

    # Method to add new child nodes
    def add_child(self, child):
        self.children.append(child) # adds the child to the current node
        child.parent = self # sets the parent of the new child to the current node

    # Method to output the ASTnode with type, values and the children
    def __repr__(self):
        return f"ASTNode({self.node_type}, {self.value}, {self.children})" # return the string representation of the node

    # Method to pretty print the AST to the console and visualiser GUI, using '--' indentation to prettily print the output of the AST right back to the user
    def pretty_print(self, indent=0):
        """
        Pretty-prints the ASTNode with '--' for each level of indentation.

        Args:
            indent (int): The current depth of the node in the tree.
        """
        # define the indentation string
        indent_str = '--' * indent # dynamically set the indent
        
        # get the value string from the node value
        value_str = f": {self.value}" if self.value is not None else ""
        
        # declare the result plus the indentation string and the type plus the value string
        result = f"{indent_str}{self.node_type}{value_str}\n"
        
        # for every child of the current node, recursively call the pretty print method
        for child in self.children:
            # indent the indentation string and pretty print that child
            result += child.pretty_print(indent + 1)
            
        # return the ast prettified
        return result

# Models the actual AST (Abstract Syntax Tree)
class AST:
    # constructor for the ast
    def __init__(self):
        # set the root to initially be none
        self.root = None

    # method to set the root of the ast
    def set_root(self, root):
        self.root = root

    # return the string representation of the AST
    def __repr__(self):
        return f"AST({self.root})"

    # method to apply pretty print to the ast
    def pretty_print(self):
        # chek if root is not none
        if self.root:
            # return the pretty print of the root
            return self.root.pretty_print()
        
        # if the root is none, return an empty string
        else:
            # tell the user the ast is empty
            return "Empty AST"

# main ast function, to create the ast from the stream of tokens from the tokeniser and validate the tokens
def create_ast_from_tokens(tokens, debug=False):
    ast = AST() # create a new AST object
    current_node = None # set the current node to none
    stack = [] # create a stack list to keep track of nodes in the staxck

    # Initialize token context
    current_token = None # set the current token to none
    previous_token = None # set the previous token to none
    next_token = None # set the next token to none

    # try and loop through the tokens to create the AST
    try:
        # create a index, and loop through the tokens
        for i, token in enumerate(tokens):
            previous_token = current_token # get the previous token
            current_token = token # get the current token
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None # get the next token

            # get the token type and value from the current token
            token_type, token_value = current_token

            # if the debug flag is sets
            if debug:
                # output token traverse, the current token, the previous token and the next token only if the debug flag is set by the user 
                print(f"DEBUG: Current token: {current_token}, Previous token: {previous_token}, Next token: {next_token}")

            # handle preprocessor directives nodes
            if token_type == "PREPROCESSOR":
                # skip the preprocessor directives
                continue

            # parse rules for keywords
            if token_type == 'KEYWORD':
                # if next token is a int
                if token_value == 'int':
                    # check if the current node is none
                    if current_node is None:
                        # create a new ASTNode for the main function
                        current_node = ASTNode("Function", "main")
                        # update the root to be the current main function one
                        ast.set_root(current_node)
                        # create a block node for the nested function contents
                        block_node = ASTNode("Block")
                        # add the block node to the current node
                        current_node.add_child(block_node)
                        # append the current node to the stack along with its chikd block node
                        stack.append(current_node)
                        # set the current node to be the block node
                        current_node = block_node
                      
                    # if not a main function it must be a variable declaration  
                    else:
                        # create a new ASTNode for the variable declarations
                        var_node = ASTNode("VariableDeclaration", None)
                        # add the var node to the current node
                        current_node.add_child(var_node)
                        # append the current node to the stack
                        stack.append(current_node)
                        # set the current node to be the variable declaration node
                        current_node = var_node

                # parse rule for returns
                elif token_value == 'return':
                    # check if return is not in a function or block scope
                    while current_node.node_type not in {"Block", "Function"}:
                        # pop the current node from the stack
                        current_node = stack.pop()
                        
                    # create a new ASTNode for the return statement
                    return_node = ASTNode("Return")
                    # add the return node to the current node
                    current_node.add_child(return_node)
                    # set the current node to be the return node
                    stack.append(current_node)
                    # update the current node to be the return node
                    current_node = return_node

                # parse rule for printf calls
                elif token_value == 'printf':
                    # create the functional call node
                    func_call_node = ASTNode("FunctionCall", token_value)
                    # add the function call node to the current node
                    current_node.add_child(func_call_node)
                    # append the current node to the stack
                    stack.append(current_node)
                    
                    # update the current node to be the function call node
                    current_node = func_call_node

            # parse rules for identifiers
            elif token_type == 'IDENTIFIER':
                # check if in function call or variable declaration
                if current_node.node_type == "FunctionCall":
                    # if in identifier, create a new identifier node
                    id_node = ASTNode("Identifier", token_value)
                    # add the identifier node to the current node
                    current_node.add_child(id_node)
                    
                # else if the current node is a variable declaration
                elif current_node.node_type == "VariableDeclaration":
                    # set the value of the current node to be the identifier value
                    current_node.value = token_value
                    
                # check if the current node is a assignment node
                elif current_node.node_type == "Assignment":
                    # create the left operand node for the identifier
                    left_operand_node = ASTNode("Identifier", token_value)
                    
                    # check for a symbol
                    if next_token and next_token[0] == 'SYMBOL' and next_token[1] in {'+', '-', '*', '/'}:
                        # get the operator token as the next token
                        operator_token = next_token
                        # update the next token to be the next token after the operator
                        next_token_index = tokens.index(next_token) + 1
                        
                        # set the right operand token to be the next next token
                        right_operand_token = tokens[next_token_index] if next_token_index < len(tokens) else None

                        # parse rule for right operand
                        if right_operand_token:
                            # create a binary operation node
                            binary_op_node = ASTNode("BinaryOperation", operator_token[1])

                            # add the binary operation node to the current node
                            current_node.add_child(binary_op_node)

                            # Add the left operand to the binary operation node
                            binary_op_node.add_child(left_operand_node)

                            # Add the right operand node to the binary operation node along with the identifier and the number
                            right_operand_node = ASTNode(
                                "Identifier" if right_operand_token[0] == 'IDENTIFIER' else "Number",
                                right_operand_token[1]
                            )
                            
                            # add the right operand node to the binary operation node
                            binary_op_node.add_child(right_operand_node)
                
            # parse rules for symbols            
            elif token_type == 'SYMBOL':
                # check if the current node is opening bracket
                if token_value == '{':
                    # create a new block node
                    block_node = ASTNode("Block")
                    # add the block node to the current node
                    current_node.add_child(block_node)
                    # append the current node to the stack
                    stack.append(current_node)
                    
                    # update the current node to be the block node
                    current_node = block_node

                # check if the current node is closing brakcet
                elif token_value == '}':
                    # pop the current node from the stack
                    current_node = stack.pop()

                # check if the current node is a equal sign
                elif token_value == '=':
                    # create the assignment node
                    assign_node = ASTNode("Assignment")
                    # add the assignment node to the current node
                    current_node.add_child(assign_node)
                    # set the current node to be the assignment node
                    stack.append(current_node)
                    # update the current node to be the assignment node
                    current_node = assign_node

                # check if the current node is a semicolon
                elif token_value == ';':
                    # check if the current node is in a return, function call, assignment or variable declaration scope
                    while current_node.node_type in {"Return", "FunctionCall", "Assignment", "VariableDeclaration"}:
                        # pop the current node from the stack
                        current_node = stack.pop()

            # parse rules for strings
            elif token_type == 'STRING':
                # get the string value from the token and create a new string node
                string_node = ASTNode("String", token_value)
                # add the string node to the current node
                current_node.add_child(string_node)

            # parse rules for numbers
            elif token_type == 'NUMBER':
                # get the number value from the token and create a new number node
                number_node = ASTNode("Number", token_value)
                # add the number node to the current node
                current_node.add_child(number_node)

    # Handle AST errors
    except Exception as e: # get the error message
        error_message = f"Error creating AST: {str(e)}\n" # the error message
        error_message += f"Current token: {current_token}\n" # what the current token is
        error_message += f"Current node: {current_node}\n" # what the current node is
        error_message += f"Stack: {stack}\n" # the stack trace
        raise RuntimeError(error_message) # raises the error message

    # applying the removed unused submodule countermeasure
    remove_unused(ast)
    
    # return the final ast to the sicher compiler
    return ast