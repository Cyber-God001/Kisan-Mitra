#!/bin/bash

dir_name="$(pwd | rev | cut -d'/' -f1 | rev)"

if [[ ${dir_name} != "Kisan-Mitra" ]]
then
    echo "Command must be run from root of the project"
    exit 1
fi

source ./bot-env/bin/activate

pip freeze > requirements.txt

deactivate