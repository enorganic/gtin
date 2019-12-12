# !/usr/bin/python3
"""
This script should be run *after* ./pypi_distribute.py
"""

import os
import shutil
import warnings
from tempfile import gettempdir
from subprocess import getstatusoutput

REPOSITORY_DIRECTORY = os.path.dirname(
    os.path.dirname(
        __file__
    )
)
PACKAGE_NAME = REPOSITORY_DIRECTORY.split(
    '/'
)[-1].split('\\')[-1].replace('_', '-')


def run(command: str) -> str:
    status, output = getstatusoutput(command)
    # Create an error if a non-zero exit status is encountered
    if status and ('WARNING:' not in output):
        if 'WARNING:' in output:
            warnings.warn(output)
        else:
            raise OSError(output)
    else:
        print(output)
    return output


if __name__ == '__main__':
    try:
        # Create recipe
        directory: str = gettempdir() + '/conda-skeleton'
        os.makedirs(directory, exist_ok=True)
        package_directory = '%s/%s' % (directory, PACKAGE_NAME)
        if os.path.exists(package_directory):
            shutil.rmtree(package_directory)
        os.chdir(directory)
        run(
            'conda skeleton pypi ' + PACKAGE_NAME
        )
        # Build
        run(
            'conda config --set anaconda_upload yes'
        )
        run(
            'conda-build ' + PACKAGE_NAME
        )
    finally:
        exec(
            open(REPOSITORY_DIRECTORY + '/scripts/clean.py').read(),
            {
                '__file__':
                os.path.abspath(REPOSITORY_DIRECTORY + '/scripts/clean.py')
            }
        )

