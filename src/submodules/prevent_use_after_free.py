# Prevent Use After Free Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

# function submodule to try and remove use after free errors in an AST
def prevent_use_after_free(node):
    """
    Prevents use-after-free errors in an AST by removing or flagging invalid memory accesses.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    
    # check if node None
    if not node:
        # return if node is not as expected
        return

    # create a object to store potentially deallocated memory for after frees
    deallocated_memory = set()

    # inner function to traverse the AST and remove use-after-free errors
    def traverse_and_prevent(node):
        # get the global deallocated_memory
        nonlocal deallocated_memory

        # for any node children
        node.children = [
            # for each child node
            child for child in node.children
            # if the child node is not a memory access
            if not (child.node_type == "MemoryAccess" and child.value in deallocated_memory)
        ]

        # for each child node of the current nodes
        for child in node.children:
            # if the child node is a memory access
            if child.node_type == "MemoryDeallocation":
                # add that child to the deallocated memory set
                deallocated_memory.add(child.value)

        # for every child in the current node children
        for child in node.children:
            # run the traverse_and_prevent function on the child node to try and add dellocated memory delocations to the set by traversing the ast of sicher and seeking any deallocated memory
            traverse_and_prevent(child)

    # run the inner function recursively
    traverse_and_prevent(node)