# Prevent Double Free Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Function to try and remove double free errors in an AST
def prevent_double_free(node):
    """
    Prevents double free errors in an AST by removing redundant deallocation nodes.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    # check if the node is None
    if not node:
        # escape if the node is None
        return

    # object to keep track of deallocated memory
    deallocated_memory = set()

    # Traverse the AST and remove double free errors
    def traverse_and_prevent(node):
        # get the global deallocated_memory
        nonlocal deallocated_memory

        # for any node children
        node.children = [
            # for each child node
            child for child in node.children
            # if the child node is not a memory deallocation
            if not (child.node_type == "MemoryDeallocation" and child.value in deallocated_memory)
        ]

        # for each child node of the current nodes
        for child in node.children:
            # if the child node is a memory deallocation
            if child.node_type == "MemoryDeallocation":
                # add that node to the deallocated memory set
                deallocated_memory.add(child.value)

        # for every child in the current node children
        for child in node.children:
            # recursively call the function on the child node to try and add dellocated memory delocations to the set
            traverse_and_prevent(child)

    # run the traverse_and_prevent function on the node to try and remove double free errors from the ast
    traverse_and_prevent(node)