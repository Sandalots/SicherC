# Run the Sicher compiler on the test testing suite c source programs and record all the errors

#!/bin/bash

python3 src/sicher.py examples/add_two_ints.c --DEBUG > add_two_ints_log.txt