#!/bin/bash

gem install gemfury
python3 setup.py sdist bdist_wheel

PACKAGE=$(ls dist/ | grep tar.gz)

fury push "dist/$PACKAGE" --api-token 14RkOI-Y84ZiWqoGEoEybR3B7kT5B8MAEk
