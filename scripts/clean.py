# !python3.7

"""
@author: David Belais <david@belais.me>

This script cleans up some temporary files created by `setuptools`, `tox`, and
`pytest`.
"""

import shutil
import os

from subprocess import getstatusoutput
from urllib.parse import urljoin

os.chdir(urljoin(__file__, '../'))

package = __file__.split('/')[-3]

for file_or_directory in (
    'dist', 'build', '%s.egg-info' % package,
    '.tox', '.cache', 'venv',
    '.pytest_cache'
):
    if os.path.exists(file_or_directory):

        command = (
            'git rm -r -f --cached --ignore-unmatch "%s"' %
            file_or_directory
        )

        print(command)

        status, output = getstatusoutput(command)

        if status != 0:
            raise OSError(output)

        if os.path.exists(file_or_directory):
            shutil.rmtree(file_or_directory)
