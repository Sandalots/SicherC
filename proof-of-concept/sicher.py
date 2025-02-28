import os

# Path to the tokeniser 
tokeniser = os.path.join(os.path.dirname(__file__), 'tokeniser.py')

# Get the root directory of the SicherC project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to the source file in the root directory
source_file = os.path.join(root_dir, 'examples/buffer_overflow.c')

# Invoke the tokeniser
os.system(f'python3 {tokeniser} {source_file}')