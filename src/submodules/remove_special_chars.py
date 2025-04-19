# Remove Special Characters Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

# method to remove newline characters from printf strings in the AST, which may cause some issues as sicher has it's own rules for newline code generation
def remove_special_chars_from_printf(ast):
    """
    Removes special characters (e.g., '\n') from printf strings in the AST.

    Args:
        ast: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    
    # check if sicher has a empty or invalid AST
    if not ast or not ast.root:
        # return if invalid/unexpected ast
        return

    # method to traverse the AST and clean up printf strings
    def traverse_and_clean(node):
        # if the current node is a printf
        if node.node_type == "FunctionCall" and node.value == "printf":
            # get the string of the printf statement/node
            string_node = next((child for child in node.children if child.node_type == "String"), None)
            
            # check if valid node
            if string_node and string_node.value:
                # Remove '\n' from the string value
                string_node.value = string_node.value.replace("\\n", "")
                
        # for any child nodes apply the cleanup method
        for child in node.children:
            # apply the remove special characters method to the child node
            traverse_and_clean(child)

    # traverse the ast and clean any new lines/special characters if they exist
    traverse_and_clean(ast.root)