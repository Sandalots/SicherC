# Sandy MacDonald (2003619)
# Create debug metrics for each of the files in the testing suite


# Run the Sicher compiler on the test testing suite c source programs and record all the errors

#!/bin/bash

# check if the debug directory exists, if not create it
if [ ! -d "debug" ]; then
    mkdir debug # this directory will contain the debug output from the compiler runs below. 
fi

# The testing suite files, shoukd output debug metrics to the compiler results to the piped file
python3 src/sicher.py examples/hello_world.c --debug > debug/hello_world_log.txt # for the hello world.c file
python3 src/sicher.py examples/add_two_ints.c --debug > debug/add_two_ints_log.txt # for the add_two_ints.c file
python3 src/sicher.py examples/buffer_overflow.c --debug > debug/buffer_overflow_log.txt # for the buffer_overflow.c file
python3 src/sicher.py examples/dangling_pointer.c --debug > debug/dangling_pointer_log.txt # for the dangling_pointer.c file
python3 src/sicher.py examples/double_free.c --debug > debug/double_free_log.txt # for the double_free.c file
python3 src/sicher.py examples/tale.c --debug > debug/tale_log.txt # for the tale.c file
python3 src/sicher.py examples/uninitialised_variable.c --debug > debug/uninitialized_variable_log.txt # for the uninitialised_variable.c file
python3 src/sicher.py examples/use_after_free.c --debug > debug/use_after_free_log.txt # for the use_after_free.c file
python3 src/sicher.py examples/test.c --debug > debug/test_log.txt # for the test.c file
# python3 src/sicher.py examples/empty.c --debug > debug/empty_log.txt # for the empty.c file
# python3 src/sicher.py examples/shouldnt_be_able_to_compile-test.rb --debug > debug/shouldnt_be_able_to_compile_log.txt # for the shouldnt_be_able_to_compile-test.rb file
