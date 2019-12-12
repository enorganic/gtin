import os
from setuptools_setup_versions import install_requires

# Operate on the directory above this one
os.chdir(os.path.dirname(os.path.dirname(__file__)))
# Update `setup.py` to require currently installed versions of all packages
install_requires.update_versions()
