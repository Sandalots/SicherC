import subprocess
import os

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = ""

    def generate_code(self):
        self.code += ".data\n"
        self.code += ".LC0:\n"
        self.code += ".string \"Hello, World!\"\n"
        self.code += ".text\n"
        self.code += ".global main\n"
        self.code += "main:\n"
        self._traverse(self.ast.root)
        return self.code

    def _traverse(self, node):
        if node.node_type == "Function":
            for child in node.children:
                self._traverse(child)
        elif node.node_type == "Block":
            for child in node.children:
                self._traverse(child)
        elif node.node_type == "VariableDeclaration":
            # Handle variable declarations if needed
            pass
        elif node.node_type == "Assignment":
            # Handle assignments if needed
            pass
        elif node.node_type == "ForLoop":
            # Handle for loops if needed
            pass
        elif node.node_type == "FunctionCall":
            if node.value == "printf":
                self.code += f"adrp x0, .LC0\n"
                self.code += f"add x0, x0, :lo12:.LC0\n"
                self.code += f"bl printf\n"
        elif node.node_type == "Return":
            self.code += f"mov w0, #{node.value}\n"
            self.code += "ret\n"

    def save_code_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.code)

    def compile_to_arm64(self, source_filename, output_filename):
        try:
            # Assemble the assembly code
            subprocess.run(['as', '-o', 'output.o', source_filename], check=True)
            # Link the object file to create the binary using clang
            subprocess.run(['clang', '-o', output_filename, 'output.o', '-target', 'arm64-apple-macos11'], check=True)
            print(f"Successfully compiled to {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")

# Example usage:
# ast = create_ast_from_tokens(tokens, debug=True)
# code_generator = CodeGenerator(ast)
# generated_code = code_generator.generate_code()
# code_generator.save_code_to_file('output.s')
# code_generator.compile_to_arm64('output.s', 'output')