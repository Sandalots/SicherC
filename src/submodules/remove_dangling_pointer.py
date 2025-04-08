# remove dangling pointer Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

def remove_dangling_pointers(node):
    """
    Removes dangling pointers from an AST.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    if not node:
        return

    # Collect valid memory allocations
    valid_memory = set()

    # First pass: Identify memory allocations and deallocations
    def collect_memory_info(node):
        if node.node_type == "MemoryAllocation":
            # Add allocated memory to the valid set
            valid_memory.add(node.value)
        elif node.node_type == "MemoryDeallocation":
            # Remove deallocated memory from the valid set
            if node.value in valid_memory:
                valid_memory.remove(node.value)
        for child in node.children:
            collect_memory_info(child)

    collect_memory_info(node)

    # Second pass: Remove dangling pointers
    def remove_invalid_pointers(node):
        node.children = [
            child for child in node.children
            if not (child.node_type == "Pointer" and child.value not in valid_memory)
        ]
        for child in node.children:
            remove_invalid_pointers(child)

    remove_invalid_pointers(node)