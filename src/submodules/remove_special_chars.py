def remove_special_chars_from_printf(ast):
    """
    Removes special characters (e.g., '\n') from printf strings in the AST.

    Args:
        ast: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    if not ast or not ast.root:
        return

    def traverse_and_clean(node):
        if node.node_type == "FunctionCall" and node.value == "printf":
            # Find the String child node
            string_node = next(
                (child for child in node.children if child.node_type == "String"), None
            )
            if string_node and string_node.value:
                # Remove '\n' from the string value
                string_node.value = string_node.value.replace("\\n", "")
        for child in node.children:
            traverse_and_clean(child)

    traverse_and_clean(ast.root)