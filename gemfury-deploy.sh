#!/bin/bash

export TWINE_USERNAME=14RkOI-Y84ZiWqoGEoEybR3B7kT5B8MAEk

gem install gemfury
python setup.py sdist bdist_wheel
python -m pip install --upgrade pip
pip install setuptools wheel twine

python setup.py sdist bdist_wheel
twine upload dist/* --repository-url https://push.fury.io/prodperfect -p ""
