# Code Generator Module for Sicher
# Sandy MacDonald
# 2003619
# 2025

# Code Generator Dependencies
import llvmlite.ir as ir  # for converting the AST to LLVM IR
import llvmlite.binding as llvm  # for compiling the above IR for the target architecture/system (the OS/CPU)
import subprocess  # for generating subprocess calls in the code generation

# Code Generator Submodules
from submodules.remove_special_chars import remove_special_chars_from_printf  # for removing new line special characters

# Class to model the Sicher Code Generator (takes the AST and generates assembly code from it)
class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="module")
        self.builder = None
        self.printf = None
        self.str_counter = 0 # for iterating unique string names
        self.variables = {}  

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
        
    def _generate_unique_str_name(self):
        self.str_counter += 1
        return f".str.{self.str_counter}"

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
                
        elif node.node_type == "VariableDeclaration":
            # Allocate memory for the variable
            var_name = node.value
            var_ptr = self.builder.alloca(ir.IntType(32), name=var_name)
            self.variables[var_name] = var_ptr  # Store the memory location in the dictionary

            # Check if the variable has an Assignment child
            assignment_node = next((child for child in node.children if child.node_type == "Assignment"), None)
            if assignment_node:
                # Get the value being assigned
                value_node = next((child for child in assignment_node.children if child.node_type == "Number"), None)
                if value_node:
                    value = int(value_node.value)
                    # Store the value in the allocated memory
                    self.builder.store(ir.Constant(ir.IntType(32), value), var_ptr)

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
                    unique_str_name = self._generate_unique_str_name()
                    fmt_str = ir.GlobalVariable(
                        self.module,
                        ir.ArrayType(ir.IntType(8), len(string_value)),
                        name=unique_str_name,
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
                    if var_name in self.variables:
                        var_ptr = self.variables[var_name]  # Retrieve the memory location from the dictionary
                        var_value = self.builder.load(var_ptr, name=var_name)

                        # Create a unique format string for integers ("%d")
                        unique_str_name = self._generate_unique_str_name()
                        fmt_str = ir.GlobalVariable(
                            self.module,
                            ir.ArrayType(ir.IntType(8), len("%d\0")),
                            name=unique_str_name,
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
                        
            if node.value == "strcpy":
                # Handle strcpy function call
                dest_node = next((child for child in node.children if child.node_type == "Identifier"), None)
                src_node = next((child for child in node.children if child.node_type == "String"), None)

                if dest_node and src_node:
                    dest_var = self.variables.get(dest_node.value)
                    if not dest_var:
                        raise ValueError(f"Undefined variable: {dest_node.value}")

                    src_value = src_node.value + "\0"  # Add null terminator
                    src_str_name = self._generate_unique_str_name()
                    src_str = ir.GlobalVariable(
                        self.module,
                        ir.ArrayType(ir.IntType(8), len(src_value)),
                        name=src_str_name,
                    )
                    src_str.initializer = ir.Constant(
                        ir.ArrayType(ir.IntType(8), len(src_value)),
                        bytearray(src_value, "utf8"),
                    )
                    src_str.global_constant = True
                    src_str.linkage = "internal"
                    src_str.align = 1
                    src_ptr = self.builder.bitcast(src_str, ir.IntType(8).as_pointer())

                    # Call memcpy to copy the string
                    memcpy_ty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer(), ir.IntType(64)])
                    memcpy = ir.Function(self.module, memcpy_ty, name="llvm.memcpy.p0i8.p0i8.i64")
                    self.builder.call(memcpy, [dest_var, src_ptr, ir.Constant(ir.IntType(64), len(src_value))])
                        
            # Add a new line after the printf call
            newline_str_name = self._generate_unique_str_name()
            newline_fmt_str = ir.GlobalVariable(
                self.module,
                ir.ArrayType(ir.IntType(8), len("\n\0")),
                name=newline_str_name,
            )
            newline_fmt_str.initializer = ir.Constant(
                ir.ArrayType(ir.IntType(8), len("\n\0")),
                bytearray("\n\0", "utf8"),
            )
            newline_fmt_str.global_constant = True
            newline_fmt_str.linkage = "internal"
            newline_fmt_str.align = 1
            newline_fmt_str_ptr = self.builder.bitcast(newline_fmt_str, ir.IntType(8).as_pointer())

            # Call printf to print the new line
            self.builder.call(self.printf, [newline_fmt_str_ptr])       
                
                    
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