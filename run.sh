# Sandy MacDonald (2003619)
# Sicher run Script (to run the sicher compiler automatically)

#!/bin/bash

# check if the user has python3 in their path
if ! command -v python3 &> /dev/null
then
    # tell the user that python3 to install python3 if it is not found
    echo "python3 could not be found, please install python3"
    exit
fi

# check if the user has pip3 in their path
if ! command -v pip3 &> /dev/null
then
    # tell the user pip could not be found
    echo "pip3 could not be found, please install pip3"
    exit
fi

# run the reqiurements.sh to install the external python packages if need be
./requirements.sh

# run the sicher compiler with hello world testing suite file as input
python3 src/sicher.py examples/hello_world.c --debug --gui # uses the GUI option plus the debug option to show additional sicher compiler logs