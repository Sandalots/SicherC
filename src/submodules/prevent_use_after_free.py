# Prevent Use After Free Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

def prevent_use_after_free(node):
    """
    Prevents use-after-free errors in an AST by removing or flagging invalid memory accesses.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    if not node:
        return

    deallocated_memory = set()

    def traverse_and_prevent(node):
        nonlocal deallocated_memory

        node.children = [
            child for child in node.children
            if not (child.node_type == "MemoryAccess" and child.value in deallocated_memory)
        ]

        for child in node.children:
            if child.node_type == "MemoryDeallocation":
                deallocated_memory.add(child.value)

        for child in node.children:
            traverse_and_prevent(child)

    traverse_and_prevent(node)