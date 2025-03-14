# Code Generator Module

# Code Generator Dependencies
import llvmlite.ir as ir
import llvmlite.binding as llvm
import subprocess

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.module = ir.Module(name="module")
        self.builder = None
        self.printf = None

    def generate_code(self):
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
            self.builder.ret(ir.Constant(ir.IntType(32), 0))
        elif node.node_type == "Block":
            for child in node.children:
                self._traverse(child)
        elif node.node_type == "FunctionCall":
            if node.value == "printf":
                fmt_str = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len("Hello, World!\0")), name=".str")
                fmt_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len("Hello, World!\0")), bytearray("Hello, World!\0", "utf8"))
                fmt_str.global_constant = True
                fmt_str.linkage = 'internal'
                fmt_str.align = 1
                fmt_str_ptr = self.builder.bitcast(fmt_str, ir.IntType(8).as_pointer())
                self.builder.call(self.printf, [fmt_str_ptr])
        elif node.node_type == "Return":
            self.builder.ret(ir.Constant(ir.IntType(32), node.children[0].value))

    def save_code_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self.module))

    def compile_to_arm64(self, source_filename, output_filename):
        try:
            # Compile the LLVM IR to assembly
            llvm.initialize()
            llvm.initialize_native_target()
            llvm.initialize_native_asmprinter()
            with open(source_filename, 'r') as f:
                llvm_ir = f.read()
            mod = llvm.parse_assembly(llvm_ir)
            mod.verify()
            target = llvm.Target.from_default_triple()
            target_machine = target.create_target_machine()
            with llvm.create_mcjit_compiler(mod, target_machine) as ee:
                ee.finalize_object()
                asm = target_machine.emit_assembly(mod)
            with open('output.s', 'w') as f:
                f.write(asm)
            # Assemble the assembly code
            subprocess.run(['as', '-arch', 'arm64', '-o', 'output.o', 'output.s'], check=True)
            # Link the object file to create the binary using clang
            subprocess.run(['clang', '-o', output_filename, 'output.o', '-target', 'arm64-apple-macos11'], check=True)
            print(f"Successfully compiled to {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")