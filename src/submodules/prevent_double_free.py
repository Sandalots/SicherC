# Prevent Double Free Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

def prevent_double_free(node):
    """
    Prevents double free errors in an AST by removing redundant deallocation nodes.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    if not node:
        return

    # Track memory deallocation
    deallocated_memory = set()

    def traverse_and_prevent(node):
        nonlocal deallocated_memory

        # Filter out redundant deallocation nodes
        node.children = [
            child for child in node.children
            if not (child.node_type == "MemoryDeallocation" and child.value in deallocated_memory)
        ]

        # Add deallocated memory to the set
        for child in node.children:
            if child.node_type == "MemoryDeallocation":
                deallocated_memory.add(child.value)

        # Recursively traverse children
        for child in node.children:
            traverse_and_prevent(child)

    traverse_and_prevent(node)