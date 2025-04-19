# Unused Remover Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

# function to mark variables as used so we can determinen if they are used or not so we can remove unused ones
def mark_used_variables(node):
    """
    Recursively traverse the AST and mark VariableDeclaration nodes as used if they are referenced.
    """
    # check if current node is a assignment
    if node.node_type == "Assignment":
        # if the assignment node has children
        if node.children:
            # get the left operand of the assignment node
            left_operand = node.children[0]
            # is the left operand a identifier
            if left_operand.node_type == "Identifier":
                # get the variable name of the left operand
                variable_name = left_operand.value
                # mark the variable as used
                mark_variable_as_used(node, variable_name)

    # check if the current node is a function call
    elif node.node_type == "FunctionCall":
        # for any children of the function call node
        for child in node.children:
            # if the child node is a identifier
            if child.node_type == "Identifier":
                # get the variable name of the child node
                variable_name = child.value
                # mark the variable as used by passing it the above variable name
                mark_variable_as_used(node, variable_name)

    # check if the current node is a binary operation
    elif node.node_type == "BinaryOperation":
        # Mark variables used in binary operations
        for child in node.children:
            # if the child node is a identifier
            if child.node_type == "Identifier":
                # get the variable name of the child node
                variable_name = child.value
                # mark the variable as used by passing it the above variable name
                mark_variable_as_used(node, variable_name)

    # Recursively check all children
    for child in node.children:
        # recursively call the function to mark any used variables in the child node
        mark_used_variables(child)

# this function marks a node used if it is indeed used later on in the ast
def mark_variable_as_used(node, variable_name):
    """
    Traverse up the AST to find the VariableDeclaration node for the given variable name and mark it as used.
    """
    # while a node has children
    while node:
        # for each child node of the current node
        for child in node.children:
            # check if current node is a variable declaration and has the same name as the variable name
            if child.node_type == "VariableDeclaration" and child.value == variable_name:
                # mark the variable as used
                child.isUsed = True
                # exit out of the while loop
                return
            
        # set the current node to the parent node
        node = node.parent

# given a node this function tries and removes any unused variables from the AST
def remove_unused_variables(node):
    """
    Recursively traverse the AST and remove VariableDeclaration nodes that are not used.
    """
    # create a unused nodes list
    unused_nodes = []
    
    # for all childrne of the current node
    for child in node.children:
        # if the child node is a variable declaration and is not used
        if child.node_type == "VariableDeclaration" and not child.isUsed:
            # add the current child to the unused nodes list
            unused_nodes.append(child)
            
        else:
            # call the function recursively on the child node so its child nodes will be checked for unused variables
            remove_unused_variables(child)

    # for each unused node in the unused nodes list
    for unused_node in unused_nodes:
        # remove the unused node from the current node's children in the AST
        node.children.remove(unused_node)
        
        # tell the user the unused node has been removed
        print(f"Removed unused variable: {unused_node.value}")

# function to remove any unused variables from the sicher ast
def remove_unused(ast):
    """
    Main function to remove unused variables from the AST.
    """
    # check if the AST is not empty
    if ast.root:
        # Mark all used variables
        mark_used_variables(ast.root)

        # Remove unused variables
        remove_unused_variables(ast.root)