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
        self.ast = ast # getting the ast of the source code created by sicher
        self.module = ir.Module(name="module")  # create a module for the code generation
        self.builder = None # create empty builder for the module
        self.printf = None # set a placeholder for any printf functions to be encountered later on
        self.str_counter = 0 # for iterating unique string names
        self.variables = {} # for storing variables

    # the function to generate the code
    def generate_code(self):
        # check if ast exists and is valid
        if self.ast is None or self.ast.root is None:
            raise ValueError("AST is empty or not initialized.")
        
        # use the remove special chars runtime submodule
        remove_special_chars_from_printf(self.ast)
        
        # printf preprocessing
        self._create_printf_function()
        
        # traverse the AST and create some code
        self._traverse(self.ast.root)
        
        # return the generated code as a string so we can capture what sicher just code generated to the user
        return str(self.module)

    # pre-processing for the printf nodes
    def _create_printf_function(self):
        # create a void pointer for the printf
        voidptr_ty = ir.IntType(8).as_pointer()
        
        # handler for a prinf function type
        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        
        # fully pre-process the printf node
        self.printf = ir.Function(self.module, printf_ty, name="printf")
        
    # creating unique assembly names for the strings so we can have multiple strings
    def _generate_unique_str_name(self):
        self.str_counter += 1 # increment the string counter
        return f".str.{self.str_counter}" # return the new incremented string name

    # function to traverse the ast and generate the code
    def _traverse(self, node):
        # check if current node is a function
        if node.node_type == "Function":
            # set the function type
            func_ty = ir.FunctionType(ir.IntType(32), [])
            # get the function
            func = ir.Function(self.module, func_ty, name=node.value)
            # create a block
            block = func.append_basic_block(name="entry")
            # set the builder to the block
            self.builder = ir.IRBuilder(block)

            # for each child of the function node
            for child in node.children:
                # traverse and generate code for each child
                self._traverse(child)

        # check if current node is a block node
        elif node.node_type == "Block":
            return_node = None  # Track the Return node to process it last
            
            # for each child of the block node
            for child in node.children:
                
                # check if the child is a return node
                if child.node_type == "Return":
                    # set the return node to the child
                    return_node = child
                    
                # if not a return node, traverse the child
                else:
                    # traverse the child and coede generate it
                    self._traverse(child)
                    
            # Process the Return node after all other nodes
            if return_node:
                # traverse the return node and code generate it
                self._traverse(return_node)
                
        # check if current node is a variable declaration
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

        # check if current node is an function call
        elif node.node_type == "FunctionCall":
            # check if the function call is a printf
            if node.value == "printf":
                # Retrieve the string argument from the FunctionCall node's children if it exists
                string_node = next((child for child in node.children if child.node_type == "String"), None ) # for a string node
                
                # get the identifier node from the function call if one exists
                identifier_node = next((child for child in node.children if child.node_type == "Identifier"), None) # for an identifier node
                
                # if the printf function has a string as an argument
                if string_node:
                    # get the value of the string node
                    string_value = string_node.value + "\0"  # Add null terminator
                    
                    # create a unique .str name for the string
                    unique_str_name = self._generate_unique_str_name()
                    
                    # create the string variable in the module
                    fmt_str = ir.GlobalVariable(
                        self.module,
                        ir.ArrayType(ir.IntType(8), len(string_value)),
                        name=unique_str_name,
                    )
                    
                    # initialise the string variable with the string value
                    fmt_str.initializer = ir.Constant(
                        ir.ArrayType(ir.IntType(8), len(string_value)),
                        bytearray(string_value, "utf8"),
                    )
                    
                    # properties of the string variable
                    fmt_str.global_constant = True 
                    fmt_str.linkage = "internal"
                    fmt_str.align = 1
                    fmt_str_ptr = self.builder.bitcast(fmt_str, ir.IntType(8).as_pointer()) # get the pointer to the string variable

                    # Call printf with the dynamically retrieved string
                    self.builder.call(self.printf, [fmt_str_ptr]) # using the printf function to print the string referencing the pointer of the above created string
                    
                # if the printf function has an identifier (variable) as an argument
                if identifier_node:
                    # get the variable name from the identifier node
                    var_name = identifier_node.value
                    
                    # check if the variable exists in the variables dictionary
                    if var_name in self.variables:
                        var_ptr = self.variables[var_name]  # Retrieve the pointer to the variable
                        var_value = self.builder.load(var_ptr, name=var_name) # get the value of the variable

                        # Create a unique .str name for the format string
                        unique_str_name = self._generate_unique_str_name()
                        
                        # Create the format string variable in the module
                        fmt_str = ir.GlobalVariable(
                            self.module,
                            ir.ArrayType(ir.IntType(8), len("%d\0")),
                            name=unique_str_name,
                        )
                        
                        # Initialise the format string variable with the format specifier
                        fmt_str.initializer = ir.Constant(
                            ir.ArrayType(ir.IntType(8), len("%d\0")),
                            bytearray("%d\0", "utf8"),
                        )
                        
                        # Properties of the format string variable
                        fmt_str.global_constant = True
                        fmt_str.linkage = "internal"
                        fmt_str.align = 1
                        fmt_str_ptr = self.builder.bitcast(fmt_str, ir.IntType(8).as_pointer()) # get the pointer to the format string variable

                        # Call printf with the variable value
                        self.builder.call(self.printf, [fmt_str_ptr, var_value]) # use both the value of the var and the pointer to the format stirng to code generate a identifier printf node
                    
            # if the function call is a strcpy method node    
            if node.value == "strcpy":
                # setup the destinatoin and source node
                dest_node = next((child for child in node.children if child.node_type == "Identifier"), None) # destination node
                src_node = next((child for child in node.children if child.node_type == "String"), None) # source node

                # check if both the destination and source nodes exist
                if dest_node and src_node:
                    # get the value of the destination node
                    dest_var = self.variables.get(dest_node.value)
                    
                    # if the value of the desintation does not exst or is undefined
                    if not dest_var:
                        # tell the user that a value error has occurred with the destination node as a undefined variable and the value of the destination node that is undefined
                        raise ValueError(f"Undefined variable: {dest_node.value}")


                    # get the value of the source node
                    src_value = src_node.value + "\0"  # Add null terminator onto the string value
                    
                    # create a unique .str name for the source string
                    src_str_name = self._generate_unique_str_name()
                    
                    # create the source string variable in the module
                    src_str = ir.GlobalVariable(
                        self.module,
                        ir.ArrayType(ir.IntType(8), len(src_value)),
                        name=src_str_name,
                    )
                    
                    # initialise the source string variable with the string value
                    src_str.initializer = ir.Constant(
                        ir.ArrayType(ir.IntType(8), len(src_value)),
                        bytearray(src_value, "utf8"),
                    )
                    
                    # properties of the source string variable
                    src_str.global_constant = True
                    src_str.linkage = "internal"
                    src_str.align = 1
                    src_ptr = self.builder.bitcast(src_str, ir.IntType(8).as_pointer()) # get the pointer to the source string variable

                    # Call memcpy to copy the string
                    memcpy_ty = ir.FunctionType(ir.VoidType(), [ir.IntType(8).as_pointer(), ir.IntType(8).as_pointer(), ir.IntType(64)]) # create the memcpy function type 
                    memcpy = ir.Function(self.module, memcpy_ty, name="llvm.memcpy.p0i8.p0i8.i64") # create the memcpy function
                    self.builder.call(memcpy, [dest_var, src_ptr, ir.Constant(ir.IntType(64), len(src_value))]) # build the memcpy function call along with the destination value and the source location pointer
                        
            # Add a new line after the printf call
            # setup a unique new line string name
            newline_str_name = self._generate_unique_str_name()
            
            # format the new line string
            newline_fmt_str = ir.GlobalVariable(
                self.module,
                ir.ArrayType(ir.IntType(8), len("\n\0")),
                name=newline_str_name,
            )
            
            # initialise the new line string
            newline_fmt_str.initializer = ir.Constant(
                ir.ArrayType(ir.IntType(8), len("\n\0")),
                bytearray("\n\0", "utf8"),
            )
            
            # properties of the new line string
            newline_fmt_str.global_constant = True
            newline_fmt_str.linkage = "internal"
            newline_fmt_str.align = 1
            newline_fmt_str_ptr = self.builder.bitcast(newline_fmt_str, ir.IntType(8).as_pointer()) # get the pointer to the new line string variable

            # Call printf to print the new line
            self.builder.call(self.printf, [newline_fmt_str_ptr]) # build the new line string variable using the pointer to the new line string formatted variable
                
        # check if current node is a return node/statement        
        elif node.node_type == "Return":
            # declare and get the return value
            return_value = ir.Constant(ir.IntType(32), int(node.children[0].value))
            # code generate the return value
            self.builder.ret(return_value)

    # function to save the generated code to a file, this file can be specified by the user either in CLI or using the Sicher GUI later on
    def save_code_to_file(self, filename):
        # try and open the filename to write to
        with open(filename, "w") as file:
            # write the code to the file
            file.write(str(self.module))

    # function to compile the generate code to arm64 assembly code
    def compile_to_arm64(self, source_filename, output_filename):
        try:
            # Initialize LLVM via llvmlite
            llvm.initialize()
            # get the native target
            llvm.initialize_native_target()
            # get the native asm printer
            llvm.initialize_native_asmprinter()

            # try and open the source filename and read the ir
            with open(source_filename, "r") as f:
                llvm_ir = f.read() # read the ir representation of the code

            # set the module to be the parsed llvm ir
            mod = llvm.parse_assembly(llvm_ir)
            
            # verify the module
            mod.verify()

            # define the target 
            target = llvm.Target.from_default_triple()
            # create the target machine
            target_machine = target.create_target_machine()

            # use the above targets and module to emit the assembly code
            with llvm.create_mcjit_compiler(mod, target_machine) as ee:
                # use the execution engine to finalise any objects
                ee.finalize_object()
                # emit the assembly code as asm uaing the target machine
                asm = target_machine.emit_assembly(mod)

            # try and write the assembly code to a file
            with open("output.s", "w") as f:
                # write the assembly contents to the file
                f.write(asm)

            # Assemble the assembly code using the arm64 assembler
            subprocess.run(["as", "-arch", "arm64", "-o", "output.o", "output.s"], check=True)

            # Link the object file to create the binary using clang for arm64 macOS platform
            subprocess.run(["clang", "-o", output_filename, "output.o", "-target", "arm64-apple-macos15"],check=True,)

            # tell the end user of what outbut binary file sicher has been code generated to
            print(f"Successfully compiled to {output_filename}")

        # Error handling any subprocess errors
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")  # tell the end user that the compilation has failed along with the error trace