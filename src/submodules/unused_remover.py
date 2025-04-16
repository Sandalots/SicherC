# Unused Remover Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

def mark_used_variables(node):
    """
    Recursively traverse the AST and mark VariableDeclaration nodes as used if they are referenced.
    """
    if node.node_type == "Assignment":
        # Mark the variable being assigned to as used
        if node.children:
            left_operand = node.children[0]
            if left_operand.node_type == "Identifier":
                variable_name = left_operand.value
                mark_variable_as_used(node, variable_name)

    elif node.node_type == "FunctionCall":
        # Mark variables used in function calls
        for child in node.children:
            if child.node_type == "Identifier":
                variable_name = child.value
                mark_variable_as_used(node, variable_name)

    # Recursively check all children
    for child in node.children:
        mark_used_variables(child)


def mark_variable_as_used(node, variable_name):
    """
    Traverse up the AST to find the VariableDeclaration node for the given variable name and mark it as used.
    """
    while node:
        for child in node.children:
            if child.node_type == "VariableDeclaration" and child.value == variable_name:
                child.isUsed = True
                return
        node = node.parent


def remove_unused_variables(node):
    """
    Recursively traverse the AST and remove VariableDeclaration nodes that are not used.
    """
    unused_nodes = []
    for child in node.children:
        if child.node_type == "VariableDeclaration" and not child.isUsed:
            unused_nodes.append(child)
        else:
            remove_unused_variables(child)

    # Remove unused nodes from the current node's children
    for unused_node in unused_nodes:
        node.children.remove(unused_node)
        print(f"Removed unused variable: {unused_node.value}")


def remove_unused(ast):
    """
    Main function to remove unused variables from the AST.
    """
    if ast.root:
        # Mark all used variables
        mark_used_variables(ast.root)

        # Remove unused variables
        remove_unused_variables(ast.root)
        