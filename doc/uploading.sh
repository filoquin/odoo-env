#!/usr/bin/env bash

# Generating distribution archives
# ################################

# verify last version
sudo python3 -m pip install --user --upgrade setuptools wheel twine

# ejecutar en el directorio donde esta setup.py
sudo python3 setup.py sdist bdist_wheel

# Uploading the distribution archives

twine upload dist/*

# luego el proyecto se puede ver en
# https://pypi.org/project/odoo-env/

# Installing your newly uploaded package
# pip install odoo-env
