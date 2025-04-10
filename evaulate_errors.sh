# Run the Sicher compiler on the test testing suite c source programs and record all the errors

#!/bin/bash

# The testing suite files
python src/sicher.py examples/hello_world.c --debug > hello_world_log.txt
python3 src/sicher.py examples/add_two_ints.c --debug > add_two_ints_log.txt
