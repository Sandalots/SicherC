def remove_unused(node):
    """
    Removes unused variables from an AST.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    if not node:
        return

    declared_vars = set()
    used_vars = set()

    # First pass: Collect declared and used variables
    def collect_vars(node):
        if node.node_type == "VariableDeclaration":
            declared_vars.add(node.value)
        elif node.node_type == "Identifier":
            used_vars.add(node.value)
        for child in node.children:
            collect_vars(child)

    collect_vars(node)

    # Identify unused variables
    unused_vars = declared_vars - used_vars

    # Second pass: Remove unused variables
    def remove_unused_nodes(node):
        node.children = [
            child for child in node.children
            if not (child.node_type == "VariableDeclaration" and child.value in unused_vars)
        ]
        for child in node.children:
            remove_unused_nodes(child)

    remove_unused_nodes(node)