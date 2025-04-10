# This shell script checks if the testing suite C source files exist in the examples directory.

# check in the examples directory if the following files exist:
# - add_two_ints.c
# - buffer_overflow.c
# - danling_pointer.c
# - double_free.c
# - hello_world.c
# - tale.c
# - uninitialised_variable.c
# - use_after_free.c

#!/bin/bash

# The testing suite files
FILES=(
    "add_two_ints.c"
    "buffer_overflow.c"
    "dangling_pointer.c"
    "double_free.c"
    "hello_world.c"
    "tale.c"
    "uninitialised_variable.c"
    "use_after_free.c"
)

# The testing suite directory note that it is called examples as it can also have user created c source files as-well as the testing suite
EXAMPLES_DIR="examples"

# Check if the testing suite does not exist
if [ ! -d "$EXAMPLES_DIR" ]; then
    # tell the user that the directory does not exist
    echo "Directory $EXAMPLES_DIR does not exist."

    # exit the script with
    exit 1
fi

# Check if all the testing suite files exist in the examples directory
for FILE in "${FILES[@]}"; do
    # if the file exists 
    if [ -f "$EXAMPLES_DIR/$FILE" ]; then
        # tell the user that the file exists
        echo "File $FILE exists."

    # if the file does not exist
    else
        # tell the user that the file does not exist
        echo "File $FILE does not exist."
    fi
done

# Check if all the testing suite files exist and if so tell the user, if not tell the user that the testing suite is not complete
if [ -f "$EXAMPLES_DIR/add_two_ints.c" ] && \
   [ -f "$EXAMPLES_DIR/buffer_overflow.c" ] && \
   [ -f "$EXAMPLES_DIR/dangling_pointer.c" ] && \
   [ -f "$EXAMPLES_DIR/double_free.c" ] && \
   [ -f "$EXAMPLES_DIR/hello_world.c" ] && \
   [ -f "$EXAMPLES_DIR/tale.c" ] && \
   [ -f "$EXAMPLES_DIR/uninitialised_variable.c" ] && \
   [ -f "$EXAMPLES_DIR/use_after_free.c" ]; then

    # tell the user they are all present
    echo "All testing suite testing C source files exist."
else
    # tell the user they are not all present
    echo "Not all testing suite source files are in the examples directory."
fi