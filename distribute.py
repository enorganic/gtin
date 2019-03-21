# !python3.7
import os
from subprocess import getstatusoutput

from setuptools_setup_versions import version, install_requires

package = __file__.split('/')[-2]

# Update `setup.py` to require currently installed versions of all packages
install_requires.update_versions()

# Build
status, output = getstatusoutput(
    'py -3.7 setup.py sdist bdist_wheel upload clean --all'
    if os.name == 'nt' else
    'python3.7 setup.py sdist bdist_wheel upload clean --all'
)

print(output)

# Update the package version if there were not any errors
if status == 0:
    version.increment()

exec(open('./clean.py').read())
