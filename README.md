## Sicher C Memory Safe Compiler

### Abstract
The Sicher C Compiler is an attempt to rectify many of the common-place Memory-safety issues that plague the C Programming Language and its compilers.

Through a modular approach, forming from the lexical analysis to the code-generation, modules are therein easily extendable to provide additional features to the Sicher C Compiler.

### State
Sicher C State as of 06/04/2025.

<br><br>
Sicher contains 5 core modules that perform the complete workings of the Sicher Compiler, as-well as optional extendable submodules. A GUI visualiser is included to present all the workings of the Sicher C Compiler and allow for easy compilations.

### Modules
1. Tokeniser (Scanner)
2. Parser
3. Analyser
4. Code Generator
5. Visualiser

### Sub-Modules
1. Buffer Sizer
2. Prevent Double Free
3. Prevent Use after Free
4. Remove Dangling Pointer
5. Unused Remover

### Usage
In the root directory of SicherC run the following:

```python3 src/sicher.py examples/hello_world.c --debug --gui```

### Features
All 5 main sicher modules fully implemented.
* Tokeniser Module
* Parser Module
* Analyser Module
* Code Generator Module
* Visualiser Module
* Countermeasures Submodules

A testing suite consiting of several c source files for which the Sicher C Compiler is to be tested on is provided in the examples directory.

### Strucuture
Testing Suite in examples/ directory.
Sicher Source Code in src/ directory.
Dependencies installation shell script in /requirements.sh.
Generated binaries will usually be in the root dir here.
Modules found in src/modules.
Submodules found in src/submodules.
src/sicher.py is the entry point to sicher.