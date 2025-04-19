# Remove Dangling Pointer Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025

# function to try and find and remove any dangling pointers in the AST
def remove_dangling_pointers(node):
    """
    Removes dangling pointers from an AST.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    
    # check if the node is None
    if not node:
        # escape the submodule if the node is None or unexpected value
        return

    # create the storage for any valid memory as a python set
    valid_memory = set()

    # attempt to collect memory information on the current node in the sicher ast
    def collect_memory_info(node):
        # check if the node is a memory allocation
        if node.node_type == "MemoryAllocation":
            # add the memory allocation to the valid memory set
            valid_memory.add(node.value)
            
        # check if the node is a memory deallocation
        elif node.node_type == "MemoryDeallocation":
            # if the value is already in the valid memory set
            if node.value in valid_memory:
                # remove the memory allocation from the valid memory set
                valid_memory.remove(node.value)
                
        # for any child nodes of the current node
        for child in node.children:
            # collect memory information on the child node
            collect_memory_info(child)

    # collect memory information on the current node
    collect_memory_info(node)

    # inner functino to try and remove any invalid pointers from the AST
    def remove_invalid_pointers(node):
        # if the current node has children
        node.children = [
            # for each child node of the current node
            child for child in node.children
            # check if not a pointer or if the child is not in the valid memory set
            if not (child.node_type == "Pointer" and child.value not in valid_memory)
        ]
        
        # for each of the childrten of the current ast node
        for child in node.children:
            # recursively call the function to remove invalid pointers on the child node(s)
            remove_invalid_pointers(child)

    # run the remove invalid pointer on the current node
    remove_invalid_pointers(node)