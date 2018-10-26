import shutil
import os
from subprocess import getstatusoutput

from setuptools_setup_versions import version, install_requires

package = __file__.split(os.path.sep)[-2]

# Update `setup.py` to require currently installed versions of all packages
install_requires.update_versions()

status, output = getstatusoutput(
    'python3.7 setup.py sdist bdist_wheel upload'
)

print(output)

if status == 0:
    # Update the package version
    version.increment()

for p in (
    './dist', './build', './%s.egg-info' % package,
    './.tox', './.cache', './venv',
    './.pytest_cache'
):
    if os.path.exists(p):
        shutil.rmtree(p)
