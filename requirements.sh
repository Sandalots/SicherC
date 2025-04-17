# Sandy MacDonald (2003619)
# Requirements Installation Shell Script to install sicher python dependencies

#!/bin/bash

# This script is to install several packages that need to be installed with python pip for the Sicher C Compiler to function and run as expected.

# install the llvmlite package for use in code generation sicher module in the codegenerator.py module.
pip install llvmlite

# install wxpython for the visualiser module, the actual gui is with wxpython so I need to import it here.
pip install wxPython

# for the visualisation plots through the visualisation generate visualisatinos functionality.
pip install matplotlib