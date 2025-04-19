# Buffer Sizer Submodule for Sicher
# Sandy MacDonald
# 2003619
# 2025


# function to resize a buffer mismatched array
def resize_array(array, target_size, default_value=0):
    """
    Resizes an array to match the target size.

    Args:
        array (list): The array to be resized.
        target_size (int): The desired size of the array.
        default_value: The value to use for padding if the array is expanded. Default is 0.

    Returns:
        list: The resized array.
    """
    
    # get the current size of the array
    current_size = len(array)

    # check if the current size is greater than the target size
    if current_size > target_size:
        # reduce the array to the target size
        return array[:target_size]
    
    # check if the current size is less than the target size
    elif current_size < target_size:
        # expand the array to the target size
        return array + [default_value] * (target_size - current_size)
    
    # if none of the past rules are met, return the array as is
    else:
        return array # no change applied to the given array


# function to traversy the ast and apply the above resize method on array mismatches
def remedy_scope_mismatch(node):
    """
    Remedies scope mismatches in an AST by resizing arrays to match their expected sizes.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    
    # if current node is invalid or empty return from the submodule
    if not node:
        return # exit the submodule

    # for any children in the current node
    for child in node.children:
        # check if the child node is a array delegation and if it has a expected size
        if child.node_type == "ArrayDeclaration" and "expected_size" in child.metadata:
            # get the current size of the array
            current_size = len(child.value)
            
            # get the target size from the metadata
            target_size = child.metadata["expected_size"]
            
            # check if the current size is not equal to the target size
            if current_size != target_size:
                # tell the user the countermeasure will be applied
                print(f"Resizing array '{child.value}' from {current_size} to {target_size}")
                
                # apply the submodule to resize the array to the target size
                child.value = resize_array(child.value, target_size)
            
        # apply the rememdy scope mismatch countermeasure to the child node    
        remedy_scope_mismatch(child)