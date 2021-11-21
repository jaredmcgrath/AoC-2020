#!/bin/bash

# -------------------------------------------------------------------------
# Get environment variables from .env file
# From: https://gist.github.com/mihow/9c7f559807069a03e302605691f85572

if [ -f .env ]; then
    # Load environment variables
    # export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
    export $(cat .env | xargs)
fi

# -------------------------------------------------------------------------
# Get environment variables from script args

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -c|--conda_env)
    CONDA_ENV="$2"
    shift # past argument
    shift # past value
    ;;
    -a|--author)
    export AOC_AUTHOR="$2"
    shift # past argument
    shift # past value
    ;;
    -d|--day)
    export AOC_DAY="$2"
    shift # past argument
    shift # past value
    ;;
    -y|--year)
    export AOC_YEAR="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# If a conda environment name was supplied, we have a ref to conda install path,
# AND env is not already active, activate it.
if [ ! -z ${CONDA_ENV+x} ] && [ ! -z ${CONDA_PYTHON_EXE+x} ] && [ "${CONDA_DEFAULT_ENV}" != "${CONDA_ENV}" ]; then
    echo "Activating $CONDA_ENV"
    # Get the dirname of the conda install
    conda_bin="$(dirname $CONDA_PYTHON_EXE)"
    conda_activate="$conda_bin/activate"
    source $conda_activate $CONDA_ENV
fi

# Now that the enviornment is (hopefully) set, run the python init_day script
python3 helpers/init_day.py
