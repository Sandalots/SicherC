import subprocess
import os

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = ""

    def generate_code(self):
        self.code += "#include <stdio.h>\n\n"  # Add the include directive
        self._traverse(self.ast.root)
        return self.code

    def _traverse(self, node):
        if node.node_type == "Function":
            self.code += f"int {node.value}() {{\n"
            for child in node.children:
                self._traverse(child)
            self.code += "}\n"
        elif node.node_type == "Block":
            for child in node.children:
                self._traverse(child)
        elif node.node_type == "VariableDeclaration":
            self.code += f"char {node.value}[{node.children[1].value}];\n"
        elif node.node_type == "Assignment":
            self.code += f"{node.children[0].value} = \"{node.children[1].value}\";\n"
        elif node.node_type == "ForLoop":
            self.code += "for (int i = 0; i < 7788; i++) {\n"
            for child in node.children:
                self._traverse(child)
            self.code += "}\n"
        elif node.node_type == "FunctionCall":
            self.code += f"{node.value}("
            for i, child in enumerate(node.children):
                if i > 0:
                    self.code += ", "
                self.code += child.value
            self.code += ");\n"
        elif node.node_type == "Return":
            self.code += f"return {node.value};\n"

    def save_code_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.code)

    def compile_to_arm64(self, source_filename, output_filename):
        try:
            subprocess.run(['gcc', '-o', output_filename, source_filename, '-target', 'arm64-apple-macos11'], check=True)
            print(f"Successfully compiled to {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")

# Example usage:
# ast = create_ast_from_tokens(tokens, debug=True)
# code_generator = CodeGenerator(ast)
# generated_code = code_generator.generate_code()
# code_generator.save_code_to_file('output.c')
# code_generator.compile_to_arm64('output.c', 'output')