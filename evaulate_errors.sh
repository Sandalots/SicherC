# Run the Sicher compiler on the test testing suite c source programs and record all the errors

#!/bin/bash

# The testing suite files, shoukd output the compiler results to the piped file
python3 src/sicher.py examples/hello_world.c --debug > debug/hello_world_log.txt
python3 src/sicher.py examples/add_two_ints.c --debug > debug/add_two_ints_log.txt
python3 src/sicher.py examples/buffer_overflow.c --debug > debug/buffer_overflow_log.txt
python3 src/sicher.py examples/dangling_pointer.c --debug > debug/dangling_pointer_log.txt
python3 src/sicher.py examples/double_free.c --debug > debug/double_free_log.txt
python3 src/sicher.py examples/tale.c --debug > debug/tale_log.txt
python3 src/sicher.py examples/uninitialised_variable.c --debug > debug/uninitialized_variable_log.txt
python3 src/sicher.py examples/use_after_free.c --debug > debug/use_after_free_log.txt