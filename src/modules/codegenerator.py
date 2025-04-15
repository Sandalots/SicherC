# Code Generator Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Code Generator Dependencies
import llvmlite.ir as ir  # for converting the AST to LLVM IR
import llvmlite.binding as llvm  # for compiling the above IR for the target architecture/system (the OS/CPU)
import subprocess  # for generating subprocess calls in the code generation
import sys  # for setting the path
import os  # for getting the parent src dir to the below appending to the path

# Code Generator Submodules
from submodules.remove_special_chars import remove_special_chars_from_printf  # for removing new line special characters


# Class to model the Sicher Code Generator (takes the AST and generates assembly code from it)
class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="module")
        self.builder = None
        self.printf = None

    def generate_code(self):
        if self.ast is None or self.ast.root is None:
            raise ValueError("AST is empty or not initialized.")
        
        # use the remove special chars runtime submodule
        remove_special_chars_from_printf(self.ast)
        
        self._create_printf_function()
        self._traverse(self.ast.root)
        
        return str(self.module)

    def _create_printf_function(self):
        # Declare printf function
        voidptr_ty = ir.IntType(8).as_pointer()
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")

    def _traverse(self, node):
        if node.node_type == "Function":
            func_ty = ir.FunctionType(ir.IntType(32), [])
            func = ir.Function(self.module, func_ty, name=node.value)
            block = func.append_basic_block(name="entry")
            self.builder = ir.IRBuilder(block)

            for child in node.children:
                self._traverse(child)

        elif node.node_type == "Block":
            return_node = None  # Track the Return node to process it last
            for child in node.children:
                if child.node_type == "Return":
                    return_node = child
                else:
                    self._traverse(child)
            # Process the Return node after all other nodes
            if return_node:
                self._traverse(return_node)

        elif node.node_type == "FunctionCall":
            if node.value == "printf":
                # Retrieve the string argument from the FunctionCall node's children
                string_node = next(
                    (child for child in node.children if child.node_type == "String"), None
                )
                
                identifier_node = next(
                    (child for child in node.children if child.node_type == "Identifier"), None
                )
                
                if string_node:
                    string_value = string_node.value + "\0"  # Add null terminator
                    fmt_str = ir.GlobalVariable(
                        self.module,
                        ir.ArrayType(ir.IntType(8), len(string_value)),
                        name=".str",
                    )
                    fmt_str.initializer = ir.Constant(
                        ir.ArrayType(ir.IntType(8), len(string_value)),
                        bytearray(string_value, "utf8"),
                    )
                    fmt_str.global_constant = True
                    fmt_str.linkage = "internal"
                    fmt_str.align = 1
                    fmt_str_ptr = self.builder.bitcast(fmt_str, ir.IntType(8).as_pointer())

                    # Call printf with the dynamically retrieved string
                    self.builder.call(self.printf, [fmt_str_ptr])
                    
                if identifier_node:
                    # Handle identifiers (variables)
                    var_name = identifier_node.value
                    var_ptr = self.builder.alloca(ir.IntType(32), name=var_name)
                    var_value = self.builder.load(var_ptr, name=var_name)

                    # Create a format string for integers ("%d")
                    fmt_str = ir.GlobalVariable(
                        self.module,
                        ir.ArrayType(ir.IntType(8), len("%d\0")),
                        name=".str",
                    )
                    fmt_str.initializer = ir.Constant(
                        ir.ArrayType(ir.IntType(8), len("%d\0")),
                        bytearray("%d\0", "utf8"),
                    )
                    fmt_str.global_constant = True
                    fmt_str.linkage = "internal"
                    fmt_str.align = 1
                    fmt_str_ptr = self.builder.bitcast(fmt_str, ir.IntType(8).as_pointer())

                    # Call printf with the variable value
                    self.builder.call(self.printf, [fmt_str_ptr, var_value])
                    

        elif node.node_type == "Return":
            return_value = ir.Constant(ir.IntType(32), int(node.children[0].value))
            self.builder.ret(return_value)

    def save_code_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(str(self.module))

    def compile_to_arm64(self, source_filename, output_filename):
        try:
            # Compile the LLVM IR to assembly
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()

            with open(source_filename, "r") as f:
                llvm_ir = f.read()

            mod = llvm.parse_assembly(llvm_ir)
            mod.verify()

            target = llvm.Target.from_default_triple()
            target_machine = target.create_target_machine()

            with llvm.create_mcjit_compiler(mod, target_machine) as ee:
                ee.finalize_object()
                asm = target_machine.emit_assembly(mod)

            with open("output.s", "w") as f:
                f.write(asm)

            # Assemble the assembly code
            subprocess.run(["as", "-arch", "arm64", "-o", "output.o", "output.s"], check=True)

            # Link the object file to create the binary using clang for arm64 macOS platform
            subprocess.run(
                ["clang", "-o", output_filename, "output.o", "-target", "arm64-apple-macos15"],
                check=True,
            )

            print(f"Successfully compiled to {output_filename}")

        # Error handling any subprocess errors
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")  # tell the end user that the compilation has failed along with the error trace