## Sicher C Memory Safe Compiler

### Abstract
The Sicher C Compiler is an attempt to rectify many of the common-place Memory-safety issues that plague the C Programming Language and its compilers.

Through a modular approach, forming from the lexical analysis to the code-generation, modules are therein easily extendable to provide additional features to the Sicher C Compiler.

### State
Sicher C State as of 13/04/2025.

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
6. Remove Special Chars

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

### Shell Scripts
A shell script is given to install python dependencies for Sicher. ```requirements.sh```
A shell script is given to check if all testing suite expected source files are present and accounted for. ```check_testing_suite.sh```
A shell script will also be provided to collect debug output for each of the default testing suite files. ```evaluate_errors.sh```
A shell script is also given to both allow for installing dependencies and running the program from the root dir. ```run.sh```

### Usage
```run.sh```

### Requirements
* Python3
* Unix environment 