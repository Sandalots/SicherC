# check if the user has python3 in their path
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found, please install python3"
    exit
fi

# check if the user has pip3 in their path
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found, please install pip3"
    exit
fi

# run the reqiurements.sh to install the external python packages if need be
./requirements.sh

# run the sicher compiler with hello world testing suite file as input
python3 src/sicher.py examples/hello_world.c --debug --gui