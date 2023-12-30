#!/bin/bash

dir_name="$(pwd | rev | cut -d'/' -f1 | rev)"

if [[ ${dir_name} != "Kisan-Mitra" ]]
then
    echo "Command must be run from root of the project"
    exit 1
fi

python -m venv bot-env

source ./bot-env/bin/activate

pip install -U pip

pip install -r requirements.txt

echo "To exit the environment 'bot-env', enter the command: source bin/end-env.sh"