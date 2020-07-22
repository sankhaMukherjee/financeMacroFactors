#!/bin/bash

python3 -m venv env

# this is for bash. Activate
# it differently for different shells
#--------------------------------------
source env/bin/activate 

pip3 install --upgrade pip

if [ -e requirements.txt ]; then

    pip3 install -r requirements.txt

else

    pip3 install pytest
    pip3 install pytest-cov
    pip3 install sphinx
    pip3 install sphinx_rtd_theme
    pip3 install wheel

    pip3 freeze > requirements.txt

fi

deactivate