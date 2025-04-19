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
    
    current_size = len(array)

    if current_size > target_size:
        return array[:target_size]
    
    elif current_size < target_size:
        return array + [default_value] * (target_size - current_size)
    else:
        return array


# function to traversy the ast and apply the above resize method on array mismatches
def remedy_scope_mismatch(node):
    """
    Remedies scope mismatches in an AST by resizing arrays to match their expected sizes.

    Args:
        node: The root node of the AST.

    Returns:
        None. The AST is modified in place.
    """
    if not node:
        return

    for child in node.children:
        if child.node_type == "ArrayDeclaration" and "expected_size" in child.metadata:
            current_size = len(child.value)
            target_size = child.metadata["expected_size"]
            
            if current_size != target_size:
                print(f"Resizing array '{child.value}' from {current_size} to {target_size}")
                child.value = resize_array(child.value, target_size)
                
        remedy_scope_mismatch(child)