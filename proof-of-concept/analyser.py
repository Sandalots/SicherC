class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"ASTNode({self.node_type}, {self.value}, {self.children})"

class AST:
    def __init__(self):
        self.root = None

    def set_root(self, root):
        self.root = root

    def __repr__(self):
        return f"AST({self.root})"